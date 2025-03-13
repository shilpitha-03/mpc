#include "rrt_path_finder/corridor_finder.h"
#include <algorithm>
#include <chrono>
using namespace Eigen;
using namespace std;

safeRegionRrtStar::safeRegionRrtStar( ){ 
      cach_size  = 100;
}

safeRegionRrtStar::~safeRegionRrtStar(){ }

Eigen::Vector3d safeRegionRrtStar::computeNoiseStd(const Eigen::Vector3d& point) {
    double x = point.x();
    // Compute axial noise (σz) using the formula from the paper
    double sigma_x = 0.001063 + 0.0007278 * x + 0.003949 * x * x;

    // Compute lateral noise (σx, σy)
    double sigma_y = 0.04;
    double sigma_z = 0.04;

    return Eigen::Vector3d(sigma_x, sigma_y, sigma_z);
}

void safeRegionRrtStar::setParam( double safety_margin_, double search_margin_, double max_radius_, double sample_range_, double h_fov_, double v_fov_, bool uncertanity_ )
{   
    std::cout<<"set param called"<<std::endl;
    safety_margin = safety_margin_;
    search_margin = search_margin_;
    max_radius    = max_radius_;
    sample_range  = sample_range_;
    h_fov = h_fov_;
    v_fov = v_fov_;\
    uncertanity = uncertanity_;
}

void safeRegionRrtStar::reset()
{     
    treeDestruct();
    
    NodeList.clear();
    EndList.clear();
    invalidSet.clear();
    PathList.clear();

    best_end_ptr = new Node();
    root_node    = new Node();

    path_exist_status  = true;
    inform_status      = false;
    global_navi_status = false;
    best_distance      = INFINITY;  
}

void safeRegionRrtStar::setStartPt( Vector3d startPt, Vector3d endPt)
{
    start_pt = startPt;
    end_pt   = endPt; 

    rand_x_in = uniform_real_distribution<double>(start_pt(0) - sample_range, start_pt(0) + sample_range);
    rand_y_in = uniform_real_distribution<double>(start_pt(1) - sample_range, start_pt(1) + sample_range);
}

void safeRegionRrtStar::setPt( Vector3d startPt, Vector3d endPt, double xl, double xh, double yl, double yh, double zl, double zh,
                           double local_range, int max_iter, double sample_portion, double goal_portion, double yaw)
{
    start_pt = startPt;
    end_pt   = endPt; 
    
    x_l = xl; x_h = xh;
    y_l = yl; y_h = yh;
    z_l = zl; z_h = zh;

    bias_l = 0.0; bias_h = 1.0;
    
    eng = default_random_engine(rd()) ;
    rand_x    = uniform_real_distribution<double>(x_l, x_h);
    rand_y    = uniform_real_distribution<double>(y_l, y_h);
    rand_z    = rand_z_in = uniform_real_distribution<double>(z_l + safety_margin, z_h); //lower bound: z_l --> z_l + safety_margin
    rand_bias = uniform_real_distribution<double>(bias_l, bias_h);

    rand_x_in = uniform_real_distribution<double>(start_pt(0) - sample_range, start_pt(0) + sample_range);
    rand_y_in = uniform_real_distribution<double>(start_pt(1) - sample_range, start_pt(1) + sample_range);

    min_distance = sqrt( pow(start_pt(0) - end_pt(0), 2) + pow(start_pt(1) - end_pt(1), 2) + pow(start_pt(2) - end_pt(2), 2) );

    /* ---------- update ellipsoid ellipsoid transformation ---------- */
    /* 3D ellipsoid transformation */
    translation_inf = (start_pt + end_pt) / 2.0;

    Eigen::Vector3d xtf, ytf, ztf, downward(0, 0, -1);
    xtf = (end_pt - translation_inf).normalized();
    ytf = xtf.cross(downward).normalized();
    ztf = xtf.cross(ytf);

    rotation_inf.col(0) = xtf;
    rotation_inf.col(1) = ytf;
    rotation_inf.col(2) = ztf;

    sample_range = local_range;
    max_samples  = max_iter;
    inlier_ratio = sample_portion;
    goal_ratio   = goal_portion;
    current_yaw = yaw;

}

void safeRegionRrtStar::setInput(pcl::PointCloud<pcl::PointXYZ> cloud_in, Eigen::Vector3d origin)
{     
    kdtreeForMap.setInputCloud( cloud_in.makeShared() );  
    CloudIn = cloud_in;
    pcd_origin = origin;
}

void safeRegionRrtStar::setInputforCollision(pcl::PointCloud<pcl::PointXYZ> cloud_in)
{
    kdtreeForCollisionPred.setInputCloud(cloud_in.makeShared());
}

inline double safeRegionRrtStar::getDis(const NodePtr node1, const NodePtr node2){
      return sqrt(pow(node1->coord(0) - node2->coord(0), 2) + pow(node1->coord(1) - node2->coord(1), 2) + pow(node1->coord(2) - node2->coord(2), 2) );
}

inline double safeRegionRrtStar::getDis(const NodePtr node1, const Vector3d & pt){
      return sqrt(pow(node1->coord(0) - pt(0), 2) + pow(node1->coord(1) - pt(1), 2) + pow(node1->coord(2) - pt(2), 2) );
}

inline double safeRegionRrtStar::getDis(const Vector3d & p1, const Vector3d & p2){
      return sqrt(pow(p1(0) - p2(0), 2) + pow(p1(1) - p2(1), 2) + pow(p1(2) - p2(2), 2) );
}

inline double safeRegionRrtStar::radiusSearch( Vector3d & search_Pt)
{     
    //    return max_radius - search_margin;

    pcl::PointXYZ searchPoint;
    searchPoint.x = search_Pt(0);
    searchPoint.y = search_Pt(1);
    searchPoint.z = search_Pt(2);

    pointIdxRadiusSearch.clear();
    pointRadiusSquaredDistance.clear();

    kdtreeForMap.nearestKSearch(searchPoint, 1, pointIdxRadiusSearch, pointRadiusSquaredDistance);
    pcl::PointXYZ nearest_obstacle = CloudIn.points[pointIdxRadiusSearch[0]];
    Eigen::Vector3d obs{nearest_obstacle.x, nearest_obstacle.y, nearest_obstacle.z};
    Eigen::Vector3d obs_camera_frame = obs - pcd_origin;
    Eigen::Vector3d std_dev_vector = computeNoiseStd(obs_camera_frame);
    double search_margin_local = search_margin;
    if(uncertanity)
    {
        search_margin_local = std_dev_vector.maxCoeff()*sqrt(11.3345);
        search_margin_local = std::min(0.6, search_margin_local);
    }
    double radius = sqrt(pointRadiusSquaredDistance[0]) - search_margin_local;
    return min(radius, double(max_radius));
}

inline double safeRegionRrtStar::radiusSearchCollisionPred( Vector3d & search_Pt)
{     
    // if(getDis(search_Pt, start_pt) > sample_range + max_radius )
    //    return max_radius - search_margin;

    pcl::PointXYZ searchPoint;
    searchPoint.x = search_Pt(0);
    searchPoint.y = search_Pt(1);
    searchPoint.z = search_Pt(2);

    pointIdxRadiusSearch.clear();
    pointRadiusSquaredDistance.clear();

    kdtreeForCollisionPred.nearestKSearch(searchPoint, 1, pointIdxRadiusSearch, pointRadiusSquaredDistance);
    double radius = sqrt(pointRadiusSquaredDistance[0]) - search_margin;
    return min(radius, double(max_radius));
}

void safeRegionRrtStar::clearBranchW(NodePtr node_delete) // Weak branch cut: if a child of a node is on the current best path, keep the child
{   // std::cout<<"clear branch seg1"<<std::endl;
    if (!node_delete) {
        std::cerr << "[Error] Node to delete is null in clearBranchW()" << std::endl;
        return;
    }
    // std::cout<<"clear branch seg2, nxt-ptr size: "<<node_delete->nxtNode_ptr.size()<<std::endl;
    
    if (!node_delete->nxtNode_ptr.empty())
    {
        for (auto nodeptr : node_delete->nxtNode_ptr) 
        {
            if (!nodeptr->best) {
                // std::cout<<"clear branch seg5"<<std::endl;
                if (nodeptr->valid) {
                    // std::cout<<"clear branch seg6"<<std::endl;
                    invalidSet.push_back(nodeptr);
                }
                // std::cout<<"clear branch seg7"<<std::endl;
                nodeptr->valid = false;
                clearBranchW(nodeptr);
            }
        }
    }
}

void safeRegionRrtStar::clearBranchS(NodePtr node_delete) // Strong branch cut: no matter how, cut all nodes in this branch
{     
    for( auto nodeptr: node_delete->nxtNode_ptr ){
        if( nodeptr->valid)
            invalidSet.push_back(nodeptr);
            nodeptr->valid = false;
            clearBranchS(nodeptr);
    }
}

void safeRegionRrtStar::treePrune(NodePtr newPtr)
{     
    NodePtr ptr = newPtr;
    if( ptr->g + ptr->f > best_distance ){ // delete it and all its branches
        // std::cout<<"x:"<<ptr->coord[0]<<" y:"<<ptr->coord[1]<<" z:"<<ptr->coord[2]<<" g:"<<ptr->g<<" f:"<<ptr->f<<" bd:"<<best_distance<<std::endl;
        ptr->invalid_in_prune = true;
        ptr->valid = false;
        invalidSet.push_back(ptr);
        clearBranchS(ptr);
    }    
}

void safeRegionRrtStar::removeInvalid()
{     
    // std::cout<<"[backup debug] seg check 3"<<std::endl;

    // std::cout<<"[root debug] seg check 7"<<std::endl;

    vector<NodePtr> UpdateNodeList;
    vector<NodePtr> UpdateEndList;
    kd_clear(kdTree_);
    // std::cout<<"[root debug] seg check 8"<<std::endl;

    for(auto nodeptr:NodeList){ // Go through all nodes, record all valid ones
        if(nodeptr->valid){
          float pos[3] = {(float)nodeptr->coord(0), (float)nodeptr->coord(1), (float)nodeptr->coord(2)};
          kd_insertf(kdTree_, pos, nodeptr);

          UpdateNodeList.push_back(nodeptr);

          if( checkEnd(nodeptr))
              UpdateEndList.push_back(nodeptr);
        }
    }

    // std::cout<<"[root debug] seg check 9"<<std::endl;
    NodeList.clear();
    EndList.clear();

    NodeList = UpdateNodeList;
    EndList  = UpdateEndList;
    // std::cout<<"[root debug] seg check 10"<<std::endl;

    // Now we should deal with all invalid nodes, broken all its related connections
    for(int i = 0; i < int(invalidSet.size()); i++ ){
        NodePtr nodeptr = invalidSet[i];

        if(nodeptr->preNode_ptr != NULL){ // let this node's father forget it
            nodeptr->change = true;
            
            vector<NodePtr> child = nodeptr->preNode_ptr->nxtNode_ptr;        
            nodeptr->preNode_ptr->nxtNode_ptr.clear();
            for(auto ptr: child){
                if( ptr->change == true ) 
                    continue;
                else
                    nodeptr->preNode_ptr->nxtNode_ptr.push_back(ptr);
            }
        }
    }
    // std::cout<<"[root debug] seg check 11"<<std::endl;

    vector<NodePtr> deleteList;
    for(int i = 0; i < int(invalidSet.size()); i++ ){
        NodePtr nodeptr = invalidSet[i];

        for(auto childptr: nodeptr->nxtNode_ptr) // let this node's children forget it
        {   
            if(childptr -> valid) 
                childptr->preNode_ptr = NULL;
        }

        deleteList.push_back(nodeptr);
    }
    // std::cout<<"[root debug] seg check 12"<<std::endl;

    invalidSet.clear();
    for(int i = 0; i < int(deleteList.size()); i++)
    {
        NodePtr ptr = deleteList[i];
        if(ptr!=NULL) delete ptr;
    }
    // std::cout<<"[root debug] seg check 13"<<std::endl;

}

Eigen::Vector3d safeRegionRrtStar::getRootCoords()
{
    return root_node->coord;
}

bool safeRegionRrtStar::resetRoot(Vector3d & target_coord)
{   
    // std::cout<<"[root debug] seg check 1"<<std::endl;
    std::cout<<"[root debug] prev root: "<<root_node->coord.transpose()<<std::endl;
    std::cout<<"[root debug] new root: "<<target_coord.transpose()<<std::endl;

    NodePtr lstNode = PathList.front();
    
    if(getDis(lstNode, target_coord) < lstNode->radius){
        global_navi_status = true;
        return 1;
    }
    std::cout<<"[root debug] seg check 2"<<std::endl;

    double cost_reduction = 0;

    commit_root = target_coord;
    vector<NodePtr> cutList;
    
    for(auto nodeptr:NodeList)
    {
        nodeptr->best = false;
    }
    std::cout<<"[root debug] seg check 3"<<std::endl;

    bool delete_root = false;

    NodePtr temp_root = NULL;
    double min_dist = 1000000000.0;
    int root_index;
    for(int i=0; i<PathList.size(); i++)
    {
        if(getDis(PathList[i], target_coord) < min_dist)
        {
            min_dist = getDis(PathList[i], target_coord);
            temp_root = PathList[i];
            root_index = i;
        }
    }
    if(root_index < PathList.size() && temp_root != NULL)
    {
        std::cout<<"[segmentation error debug] commit target: "<<target_coord.transpose()<<std::endl;
        PathList[root_index]->best = true;
        PathList[root_index]->preNode_ptr = NULL;
        
        cost_reduction = PathList[root_index]->g;
        
        if((PathList[root_index]->coord -root_node->coord).norm()<0.2)
        {
            return 0;
        }
        root_node = PathList[root_index];
        std::cout<<"[segmentation error debug] new root node: "<<root_node->coord.transpose()<<std::endl;

    }
    else
    {
        std::cout<<"########### we are fucked ############"<<std::endl;
    }

    for(int i=root_index+1; i<PathList.size(); i++)
    {
        PathList[i]->best = false;
        PathList[i]->valid = false;
        cutList.push_back(PathList[i]);
    }

    // std::cout<<"[root debug] seg check 4"<<std::endl;

    solutionUpdate(cost_reduction, target_coord);
    // std::cout<<"[root debug] seg check 5"<<std::endl;

    for(auto nodeptr:cutList){
        invalidSet.push_back(nodeptr);
        clearBranchW(nodeptr);
    }
    // std::cout<<"[root debug] seg check 6"<<std::endl;

    removeInvalid();
    return 1;
}

void safeRegionRrtStar::solutionUpdate(double cost_reduction, Vector3d target)
{
    for(auto nodeptr: NodeList){
        nodeptr->g -= cost_reduction;
    }
    min_distance = getDis(target, end_pt);
    
    /* ---------- update ellipsoid transformation ---------- */
    /* 3D ellipsoid transformation */
    translation_inf = (target + end_pt) / 2.0;

    Eigen::Vector3d xtf, ytf, ztf, downward(0, 0, -1);
    xtf = (target - translation_inf).normalized();
    ytf = xtf.cross(downward).normalized();
    ztf = xtf.cross(ytf);

    rotation_inf.col(0) = xtf;
    rotation_inf.col(1) = ytf;
    rotation_inf.col(2) = ztf;

    best_distance -= cost_reduction;
}

void safeRegionRrtStar::updateHeuristicRegion(NodePtr update_end_node)
{   
    /*  This function update the heuristic hype-ellipsoid sampling region once and better path has been found  */
    // Update the up-to-date traversal and conjugate diameter of the ellipsoid.
    // If there is no improvement in the path, maintain the heuristic unchange.

    double update_cost = update_end_node->g + getDis(update_end_node, end_pt) + getDis(root_node, commit_root);

    if(update_cost < best_distance){  
        best_distance = update_cost;
        elli_l = best_distance;
        elli_s = sqrt(best_distance * best_distance - min_distance * min_distance);

        // release the old best path, free the best status
        if(inform_status){
            for(auto ptr:NodeList)
                ptr->best = false;
        }

        // update the nodes in the new best path to be marked as best
        NodePtr ptr = update_end_node;
        while( ptr != NULL  ) 
        {  
            ptr->best = true;
            ptr = ptr->preNode_ptr;
        }

        best_end_ptr = update_end_node;
    }    
}

inline Vector3d safeRegionRrtStar::genSample()
{     
    Vector3d pt;
    double bias = rand_bias(eng);
    if( bias <= goal_ratio ){
        pt = end_pt;
        return pt;
    }

    /*  Generate samples in a heuristic hype-ellipsoid region  */
    //    1. generate samples according to (rho, phi), which is a unit circle
    //    2. scale the unit circle to a ellipsoid
    //    3. rotate the ellipsoid
    if(!inform_status) { 
        if( bias > goal_ratio && bias <= (goal_ratio + inlier_ratio) ){ 
            // sample inside the local map's boundary
            pt(0)    = rand_x_in(eng);
            pt(1)    = rand_y_in(eng);
            pt(2)    = rand_z_in(eng);  
        }
        else{           
            // uniformly sample in all region
            pt(0)    = rand_x(eng);
            pt(1)    = rand_y(eng);
            pt(2)    = rand_z(eng);  
        }
    }
    else{ 
        /* ---------- uniform sample in 3D ellipsoid ---------- */
        double us = rand_u(eng);
        double vs = rand_v(eng);
        double phis = rand_phi(eng);

        /* inverse CDF */
        double as = elli_l / 2.0 * cbrt(us);
        double bs = elli_s / 2.0 * cbrt(us);
        double thetas = acos(1 - 2 * vs);

        pt(0) = as * sin(thetas) * cos(phis);
        pt(1) = bs * sin(thetas) * sin(phis);
        pt(2) = bs * cos(thetas);

        pt = rotation_inf * pt + translation_inf;

        pt(0) = min( max( pt(0), x_l ), x_h );
        pt(1) = min( max( pt(1), y_l ), y_h );
        pt(2) = min( max( pt(2), z_l ), z_h );
    }

    return pt;
}

bool safeRegionRrtStar::isInFOV(const Eigen::Vector3d& pt)
{
    Vector3d dir = pt - start_pt;
    double distance = dir.norm();
    if (distance == 0) return true;

    // Normalize direction vector
    dir.normalize();

    // Compute yaw and pitch of direction vector
    double azimuth = atan2(dir.y(), dir.x()); // Horizontal angle
    double elevation = asin(dir.z()); // Vertical angle

    // Convert UAV yaw to radians
    double yaw_rad = current_yaw;

    // Compute yaw difference and normalize to [-pi, pi]
    double yaw_diff = azimuth - yaw_rad;
    yaw_diff = atan2(sin(yaw_diff), cos(yaw_diff));

    // Check if within horizontal and vertical FOV limits
    return (fabs(yaw_diff) <= (h_fov / 2.0)) && (fabs(elevation) <= (v_fov / 2.0));
}

inline NodePtr safeRegionRrtStar::genNewNode( Vector3d & pt_sample, NodePtr node_nearst_ptr )
{
    double dis       = getDis(node_nearst_ptr, pt_sample);

    Vector3d center;
    if(dis > node_nearst_ptr->radius)
    {
        double steer_dis = node_nearst_ptr->radius / dis;
        center(0) = node_nearst_ptr->coord(0) + (pt_sample(0) - node_nearst_ptr->coord(0)) * steer_dis;
        center(1) = node_nearst_ptr->coord(1) + (pt_sample(1) - node_nearst_ptr->coord(1)) * steer_dis;
        center(2) = node_nearst_ptr->coord(2) + (pt_sample(2) - node_nearst_ptr->coord(2)) * steer_dis;
    }
    else
    {
        center(0) = pt_sample(0);
        center(1) = pt_sample(1);
        center(2) = pt_sample(2);
    }
    
    double radius_ = radiusSearch( center );
    double h_dis_  = getDis(center, end_pt);

    NodePtr node_new_ptr = new Node( center, radius_, INFINITY, h_dis_ ); 
    
    return node_new_ptr;
}

bool safeRegionRrtStar::checkTrajPtCol(Vector3d & pt)
{     
    if(radiusSearchCollisionPred(pt) < 0 ) return true;
    else return false;
}

inline bool safeRegionRrtStar::checkEnd( NodePtr ptr )
{    
    double distance = getDis(ptr, end_pt);
    
    if(distance + 0.1 < ptr->radius)
        return true;      
   
    return false;
}

inline NodePtr safeRegionRrtStar::findNearstVertex( Vector3d & pt )
{
    float pos[3] = {(float)pt(0), (float)pt(1), (float)pt(2)};
    kdres * nearest = kd_nearestf( kdTree_, pos );

    NodePtr node_nearst_ptr = (NodePtr) kd_res_item_data( nearest );
    kd_res_free(nearest);
    
    return node_nearst_ptr;
}

inline int safeRegionRrtStar::checkNodeRelation( double dis, NodePtr node_1, NodePtr node_2 )
{
// -1 indicate two nodes are connected good
//  0 indicate two nodes are not connected
//  1 indicate node_1 contains node_2, node_2 should be deleted. 

    int status;
    if( (dis + node_2->radius) == node_1->radius)
        status = 1;
    else if( (dis + 0.1) < 0.95 * (node_1->radius + node_2->radius) ) // && (dis > node_1->radius) && (dis > node_2->radius)
        status = -1;
    else
        status = 0;
    
    return status;
}

#if 1
void safeRegionRrtStar::treeRewire( NodePtr node_new_ptr, NodePtr node_nearst_ptr)
{     
      NodePtr newPtr     = node_new_ptr;      
      NodePtr nearestPtr = node_nearst_ptr;

      float range = newPtr->radius * 2.0f;
      float pos[3] = {(float)newPtr->coord(0), (float)newPtr->coord(1), (float)newPtr->coord(2)};
      struct kdres *presults  = kd_nearest_rangef( kdTree_, pos, range);

      vector<NodePtr> nearPtrList;
      bool isInvalid = false;
      while( !kd_res_end( presults ) ) { // Pull all the nodes outside the result data structure from the kd-tree
                                         // And go through all the nearby vertex, check the relations, to see whether the newPtr should be discarded
            NodePtr nearPtr = (NodePtr)kd_res_item_data( presults );

            double dis = getDis( nearPtr, newPtr );
            int   res = checkNodeRelation( dis, nearPtr, newPtr );
            nearPtr->rel_id  = res;    // temporary variables to record the local realtions with nearby nodes, to avoid repeated calculation in this two terms
            nearPtr->rel_dis = dis;

            if( res == 1 ){
                // std::cout<<"invalid in rewire"<<std::endl;
                newPtr->invalid_in_rewire = true;
                newPtr->valid = false;
                
                isInvalid = true;
                nearPtrList.push_back(nearPtr);
                break;
            }
            else{
                nearPtrList.push_back(nearPtr);
                kd_res_next( presults );
            }
      }
      kd_res_free( presults );

      if(isInvalid){
          for(auto nodeptr: nearPtrList){ // release all the temporary variables
              nodeptr->rel_id  = -2;
              nodeptr->rel_dis = -1.0;
          }
          return;
      }
      double min_cost = nearestPtr->g +  getDis( nearestPtr, newPtr );
      newPtr->preNode_ptr = nearestPtr;
      newPtr->g = min_cost;
      nearestPtr->nxtNode_ptr.push_back(newPtr);
      NodePtr lstParentPtr = nearestPtr; // a pointer records the last best father of the new node

      vector<NodePtr> nearVertex;

      /*  Go through all the nearby vertex again, to deal with another two case. Note, better not mix this go through with the previous one  */
      for(auto nodeptr:nearPtrList){
        NodePtr nearPtr = nodeptr;
        
        // Choose the parent
        int res   = nearPtr->rel_id;
        double dis = nearPtr->rel_dis;
        double cost = nearPtr->g + dis;
        
        if( res == -1 ){
            if( cost < min_cost ){ // has a shorter path if new_ptr's father is the new node
                min_cost = cost;
                newPtr->preNode_ptr = nearPtr;
                newPtr->g = min_cost;
                lstParentPtr->nxtNode_ptr.pop_back();
                lstParentPtr = nearPtr; // change a father, record the last father
                lstParentPtr->nxtNode_ptr.push_back(newPtr);
            }
            nearVertex.push_back(nearPtr);
        }      
        nearPtr->rel_id  = -2;
        nearPtr->rel_dis = -1.0;
      }

      /*  Rewire the neighbors  */
      for(int i = 0; i < int(nearVertex.size()); i++ ){
          NodePtr nodeptr = nearVertex[i];
          
          NodePtr nearPtr = nodeptr;
          if(nearPtr->valid == false) continue;

          double dis = getDis( nearPtr, newPtr );
          double cost = dis + newPtr->g;
          
          if( cost < nearPtr->g){ // a near Node changed a father, delete this node from its parent's childer list
              
              if(isSuccessor(nearPtr, newPtr->preNode_ptr)) 
                  continue; // By experiments, this function does work here
              
              if(nearPtr->preNode_ptr == NULL ){
                  nearPtr->preNode_ptr = newPtr;
                  nearPtr->g = cost;
              }
              else{
                  NodePtr lstNearParent = nearPtr->preNode_ptr;
                  nearPtr->preNode_ptr = newPtr;
                  nearPtr->g = cost;
                  
                  nearPtr->change = true; // use a temporary flag to indicate this pointer should be deleted
                  vector<NodePtr> child = lstNearParent->nxtNode_ptr;
                      
                  lstNearParent->nxtNode_ptr.clear();
                  for(auto ptr: child){
                      if( ptr->change == true ) continue;
                      else lstNearParent->nxtNode_ptr.push_back(ptr);
                  }
                  nearPtr->change = false; // release the flag after the delete  
              }
            
              newPtr->nxtNode_ptr.push_back(nearPtr);
          }
      }
}
#endif

void safeRegionRrtStar::recordNode(NodePtr new_node)
{
    NodeList.push_back(new_node);
}

void safeRegionRrtStar::tracePath()
{   
    vector<NodePtr> feasibleEndList;      
    for(auto endPtr: EndList)
    {
        if( (checkValidEnd(endPtr) == false) || (checkEnd(endPtr) == false) || (endPtr->valid == false) )
        {
            std::cout<<"endPtr pos"<<endPtr->coord<<" radius: "<<endPtr->radius<<std::endl;

            continue;
        }
        else
            feasibleEndList.push_back(endPtr);
    }

    if( int(feasibleEndList.size()) == 0 )
    {
        std::cout<<"[trace path] can't find a feasible path. "<<std::endl;
        path_exist_status = false;
        best_distance = INFINITY;
        inform_status = false;
        EndList.clear();
        Path   = Eigen::MatrixXd::Identity(3,3);
        Radius = Eigen::VectorXd::Zero(3);
        return;
    }

    EndList = feasibleEndList;

    best_end_ptr = feasibleEndList[0];
    double best_cost = INFINITY;
    for(auto nodeptr: feasibleEndList)
    {   
        double cost = (nodeptr->g + getDis(nodeptr, end_pt) + getDis(root_node, commit_root) );
        if( cost < best_cost )
        {
            best_end_ptr  = nodeptr;
            best_cost = cost;
            best_distance = best_cost;
        }
    }

    NodePtr ptr = best_end_ptr;

    /*  stack the path (corridor) data for trajectory generation  */
    int idx = 0;
    PathList.clear();

    while( ptr != NULL ) {
        // std::cout<<"point: "<<ptr->coord[0]<<" : "<<ptr->coord[1]<<" : "<<ptr->coord[2]<<std::endl; 
        PathList.push_back( ptr );
        ptr = ptr->preNode_ptr;
        idx ++;
    }

    Path.resize(idx, 3) ;
    Radius.resize( idx );
    idx = 0;
    
    ptr = best_end_ptr;
    idx ++ ;

    while( ptr != NULL ){      
          Path.row(Path.rows() - idx) = ptr->coord;
          Radius(Radius.size() - idx) = ptr->radius;
          
          ptr = ptr->preNode_ptr;
          idx ++;
    }

    path_exist_status = true;
}

void safeRegionRrtStar::treeDestruct()
{
    if(kdTree_ != NULL)
    {
        kd_free(kdTree_);
    }
    
    for( int i = 0; i < int(NodeList.size()); i++)
    {   
        NodePtr ptr = NodeList[i];
        if(ptr != NULL)
        {
            delete ptr;
        }
    }
}

inline double safeRegionRrtStar::checkRadius(Vector3d & pt)
{
    return radiusSearch( pt );
}

inline int safeRegionRrtStar::checkNodeUpdate(double new_radius, double old_radius)
{
    if( new_radius < safety_margin)  
        return -1; // for not qualified, this node should be deleted
    else if( new_radius < old_radius )
        return 0;  // for node radius shrink, this node should be inspected for connection with others 
    else 
        return 1;  // for no difference, nothing should be changed
}


inline bool safeRegionRrtStar::isSuccessor(NodePtr curPtr, NodePtr nearPtr) // check if curPtr is father of nearPtr
{     
    NodePtr prePtr = nearPtr->preNode_ptr;
    
    while(prePtr != NULL)
    {
        if(prePtr == curPtr) return true;
        else
          prePtr = prePtr->preNode_ptr;
    }

    return false;
}

inline bool safeRegionRrtStar::checkValidEnd(NodePtr endPtr)
{
    NodePtr ptr = endPtr;

    while( ptr != NULL )
    {   
        if(!ptr->valid) 
          return false;
  
        if( getDis( ptr, root_node->coord ) < ptr->radius )
          return true;

        ptr = ptr->preNode_ptr;
    }

    return false;  
}

void safeRegionRrtStar::SafeRegionExpansion( double time_limit )
{   
    /*  The initialization of the safe region RRT* tree  */
    auto time_bef_expand = std::chrono::steady_clock::now();
    kdTree_ = kd_create(3);
    commit_root  = start_pt;
    root_node = new Node(start_pt, radiusSearch( start_pt ), 0.0, min_distance); 

    recordNode(root_node);

    float pos[3] = {(float)root_node->coord(0), (float)root_node->coord(1), (float)root_node->coord(2)};
    kd_insertf(kdTree_, pos, root_node);
    int iter_count;

    for( iter_count = 0; iter_count < max_samples; iter_count ++)
    {     
        auto time_in_expand = std::chrono::steady_clock::now();
        auto elapsed = std::chrono::duration_cast<std::chrono::milliseconds>(time_in_expand - time_bef_expand).count()*0.001;
        if( elapsed > time_limit ) break;
        
        Vector3d   pt_sample = genSample();
        sampleList.push_back(pt_sample);
        
        NodePtr node_nearst_ptr = findNearstVertex(pt_sample);
        
        if(!node_nearst_ptr->valid || node_nearst_ptr == NULL )
        {
            // std::cout<<"if1"<<std::endl;
            continue;
        }

        NodePtr node_new_ptr = genNewNode(pt_sample, node_nearst_ptr); 
        
        if( node_new_ptr->coord(2) < z_l  || node_new_ptr->radius < safety_margin )
        {
            // bool a = node_new_ptr->coord(2) < z_l;
            // bool b = node_new_ptr->radius < safety_margin;
            // std::cout<<node_new_ptr->radius<<":"<<safety_margin<<std::endl;
            continue;
        }
        
        treeRewire(node_new_ptr, node_nearst_ptr);  
        
        if( ! node_new_ptr->valid)
        {
            // std::cout<<"if3"<<std::endl;
            continue;
        }

        if(checkEnd( node_new_ptr ))
        {
            if( !inform_status ) best_end_ptr = node_new_ptr;
            
            EndList.push_back(node_new_ptr);
            updateHeuristicRegion(node_new_ptr);
            inform_status = true;  
        }
        
        pos[0] = (float)node_new_ptr->coord(0);
        pos[1] = (float)node_new_ptr->coord(1);
        pos[2] = (float)node_new_ptr->coord(2);
        kd_insertf(kdTree_, pos, node_new_ptr);

        recordNode(node_new_ptr);
        // std::cout<<"inserted node coord: "<<node_new_ptr->coord[0]<<" : "<<node_new_ptr->coord[1]<<" : "<<node_new_ptr->coord[2]<<std::endl;
        selectedNodeList.push_back(node_new_ptr->coord);
        treePrune(node_new_ptr);      

        if( int(invalidSet.size()) >= cach_size) removeInvalid();
    }

    removeInvalid();
    tracePath();

}

void safeRegionRrtStar::SafeRegionRefine( double time_limit )
{   
    /*  Every time the refine function is called, new samples are continuously generated and the tree is continuously rewired, hope to get a better solution  */
    /*  The refine process is mainly same as the initialization of the tree  */
    auto time_bef_refine = std::chrono::steady_clock::now();
    // std::cout<<"in refine loop"<<std::endl;
    float pos[3];
    while( true )
    {     
        auto time_in_refine = std::chrono::steady_clock::now();
        auto elapsed = std::chrono::duration_cast<std::chrono::milliseconds>(time_in_refine - time_bef_refine).count()*0.001;
        if( elapsed > time_limit )
        {
            // std::cout<<"[refine debug] time in refine loop: "<<elapsed<<" time limit: "<<time_limit<<std::endl;
            break;
        } 
        
        Vector3d pt_sample =  genSample();
        NodePtr node_nearst_ptr = findNearstVertex(pt_sample);
        
        if(!node_nearst_ptr->valid || node_nearst_ptr == NULL ) continue;
                  
        NodePtr node_new_ptr  =  genNewNode(pt_sample, node_nearst_ptr); 
        
        if( node_new_ptr->coord(2) < z_l  || node_new_ptr->radius < safety_margin ) continue;
           
        treeRewire(node_new_ptr, node_nearst_ptr);  
        
        if( node_new_ptr->valid == false ) continue;

        if(checkEnd( node_new_ptr )){
            if( !inform_status ) 
                best_end_ptr = node_new_ptr;
            
            EndList.push_back(node_new_ptr);
            updateHeuristicRegion(node_new_ptr);
            inform_status = true;  
        }
        
        pos[0] = (float)node_new_ptr->coord(0);
        pos[1] = (float)node_new_ptr->coord(1);
        pos[2] = (float)node_new_ptr->coord(2);
        kd_insertf(kdTree_, pos, node_new_ptr);

        recordNode(node_new_ptr);
        treePrune(node_new_ptr);      
        if( int(invalidSet.size()) >= cach_size) removeInvalid();
  }

    removeInvalid();    
    tracePath();

}

void safeRegionRrtStar::SafeRegionEvaluate( double time_limit )
{   
    /*  The re-evaluate of the RRT*, find the best feasble path (corridor) by lazy-evaluzation  */
    if(path_exist_status == false){
        // std::cout<<"[path re-evaluate] no path exists. "<<std::endl;
        return;
    }
    
    auto time_bef_evaluate = std::chrono::steady_clock::now();

    vector< pair<Vector3d, double> > fail_node_list;
    while(true)
    {   
        for(int i = 0; i < int(PathList.size()); i++ ) 
        {   
            NodePtr ptr = PathList[i];
            NodePtr pre_ptr =  ptr->preNode_ptr;

            if( pre_ptr != NULL ){
                double update_radius = checkRadius(ptr->coord);
                int ret = checkNodeUpdate(update_radius, ptr->radius); // -1: not qualified, 0: shrink, 1: no difference, continue
                double old_radius = ptr->radius;
                ptr->radius = update_radius; // the radius of a node may shrink or remain no change, but can not enlarge

                if( ret == -1){   
                    // The node ptr now does't have enough volume for the robot to pass, the node should be deleted from the tree; 
                    // all its child nodes should be put in the rewire list 
                    ptr->valid = false;          // Delete this node
                    invalidSet.push_back(ptr);
                    clearBranchS(ptr);
                    fail_node_list.push_back(make_pair(ptr->coord, old_radius));
                }
                else 
                {   // Test whether the node disconnected with its parent and all children,
                    // If disconnect with parent, delete it, if discoonect with a child, delete the child
                    if( checkNodeRelation( getDis( ptr, pre_ptr ), ptr, pre_ptr ) != -1 ) {
                        // the child is disconnected with its parent   
                        if(ptr->valid == true){
                            ptr->valid = false;      
                            invalidSet.push_back(ptr);
                            clearBranchS(ptr);
                            fail_node_list.push_back(make_pair(ptr->coord, old_radius));
                        }
                    } 
                    else
                    {
                        vector<NodePtr> childList = ptr->nxtNode_ptr;
                        for(auto nodeptr: childList){  
                            // inspect each child of ptr, to see whether they are still connected 
                            int res = checkNodeRelation( getDis( ptr, nodeptr ), ptr, nodeptr );
                            if( res != -1 ) {   
                                // the child is disconnected with its parent
                                if(nodeptr->valid == true){
                                    nodeptr->valid = false;      
                                    invalidSet.push_back(nodeptr);
                                    clearBranchS(nodeptr);
                                    fail_node_list.push_back(make_pair(nodeptr->coord, nodeptr->radius));
                                }
                            } 
                        }
                    }
                }
            }
        }

        bool isBreak = true;

        for(auto ptr:PathList) 
          isBreak = isBreak && ptr->valid;
        
        auto time_in_evaluate2 = std::chrono::steady_clock::now();

        if(isBreak)
        {
            // std::cout<<"[evaluate debug] break condition reached: time in evaluate: "<<std::chrono::duration_cast<std::chrono::milliseconds>(time_in_evaluate2 - time_bef_evaluate).count()*0.001<<std::endl;
            break;
        }

        vector<NodePtr> feasibleEndList;                
        for(auto endPtr: EndList)
        {
            if( (endPtr->valid == false)  || (checkEnd(endPtr) == false) )
                continue;
            else
                feasibleEndList.push_back(endPtr);
        }


        EndList = feasibleEndList;
        auto time_in_evaluate = std::chrono::steady_clock::now();
        auto elapsed = std::chrono::duration_cast<std::chrono::milliseconds>(time_in_evaluate - time_bef_evaluate).count()*0.001;
        if(feasibleEndList.size() == 0 || elapsed > time_limit ){
            path_exist_status = false;
            inform_status = false;
            best_distance = INFINITY;
            break;
        }
        else{
            best_end_ptr = feasibleEndList[0];
            double best_cost = INFINITY;
            for(auto nodeptr: feasibleEndList)
            {
                double cost = (nodeptr->g + getDis(nodeptr, end_pt) + getDis(root_node, commit_root) );
                if( cost < best_cost ){
                    best_end_ptr  = nodeptr;
                    best_cost = cost;
                    best_distance = best_cost;
                }
            }
        
            PathList.clear();
            NodePtr ptrr = best_end_ptr;
            while( ptrr != NULL )
            {
                PathList.push_back( ptrr );
                ptrr = ptrr->preNode_ptr;
            }
        }
    } 
    
    auto time_aft_evaluate = std::chrono::steady_clock::now();
    double repair_limit = time_limit - std::chrono::duration_cast<std::chrono::milliseconds>(time_aft_evaluate - time_bef_evaluate).count()*0.001;

    removeInvalid();
    treeRepair(repair_limit, fail_node_list); /*  This function is optional, better turn on to improve path quality  */
    tracePath();
}

void safeRegionRrtStar::treeRepair(double time_limit, vector< pair<Vector3d, double> > & node_list)
{   
    /*  This function is optional  */
    /*  Use this function to improve the success rate of the tree refinement  */

    // check nearby nodes in all the failure nodes' neighbour, 
    // try to repair the tree, since where the nodes failed should most possibly fail again
    int repairSize = int(node_list.size());

    auto time_bef_repair = std::chrono::steady_clock::now();
    for(int i = 0; i < repairSize; i++)
    {   
        auto time_in_repair = std::chrono::steady_clock::now();
        auto elapsed = std::chrono::duration_cast<std::chrono::milliseconds>(time_in_repair - time_bef_repair).count()*0.001;

        if(elapsed > time_limit ) break;

        Vector3d center = node_list[i].first;
        float range  = node_list[i].second * 2.0f;
        float pos[3] = {(float)center(0), (float)center(1), (float)center(2)};
        struct kdres *presults  = kd_nearest_rangef( kdTree_, pos, range);

        while( !kd_res_end( presults ) ) 
        { 
            NodePtr ptr = (NodePtr)kd_res_item_data( presults );
            
            if(ptr->valid == false){   
                kd_res_next( presults );
                continue;
            }
            
            NodePtr pre_ptr = ptr->preNode_ptr;
            
            if(pre_ptr == root_node || ptr == root_node){
                kd_res_next( presults );
                continue;
            }
            
            double update_radius = checkRadius(ptr->coord);
            int ret = checkNodeUpdate(update_radius, ptr->radius); // -1: not qualified, 0: shrink, 1: no difference, continue
            ptr->radius = update_radius; // the radius of a node may shrink or remain no change, but can not enlarge

            if( ret == -1){ // Delete this node
                if(ptr->valid == true){
                    ptr->valid = false;         
                    invalidSet.push_back(ptr);
                    clearBranchS(ptr);
                }
            }
            else {   
                double dis = getDis( pre_ptr, ptr );
                int   res = checkNodeRelation( dis, pre_ptr, ptr );
                if( res != -1 ) { // ptr and pre_ptr are not connected anymore   
                    if(pre_ptr->valid == true){
                          pre_ptr->valid = false;      
                          invalidSet.push_back(pre_ptr);
                          clearBranchS(pre_ptr);
                          kd_res_next( presults );
                          continue;
                    }
                }

                vector<NodePtr> childList = ptr->nxtNode_ptr;
                for(auto childptr: childList){  // inspect each child of ptr, to see whether they are still connected 
                    double dis = getDis( ptr, childptr );
                    int res = checkNodeRelation( dis, ptr, childptr );
                    if( res != -1 ) { // the child is disconnected with its parent   
                        if(childptr->valid == true){
                            childptr->valid = false;      
                            invalidSet.push_back(childptr);
                            clearBranchS(childptr);
                        }
                    } 
                }
            }

            kd_res_next( presults );
        }

        kd_res_free( presults );
    }
    
    removeInvalid();

}