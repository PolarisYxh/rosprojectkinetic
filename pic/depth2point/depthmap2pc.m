% Projects the given depth image to world coordinates. Note that this 3D
% coordinate space is defined by a horizontal plane made from the X and Z
% axes and the Y axis points up.
%
% Args:
%   imgDepthAbs - 480x640 depth image whose values indicate depth in
%                 meters.
%
% Returns:
%   points3d - Nx3 matrix of 3D world points (X,Y,Z).
function points3d = depth_plane2depth_world()
  imgDepthAbs = imread('./6_d.png');
%  imgDepthAbs = imread('./depth0000.jpg');
% imgDepthAbs = im2double(imgDepthAbs);
  [H, W] = size(imgDepthAbs);
%   assert(H == 1050);
%   assert(W == 1680);
  imgDepthAbs = double(imgDepthAbs);

fx_d = 2977.4229552992974;%3721.7786941241206;
fy_d = 2977.4229552992974;
cx_d = 840;
cy_d = 525;

% fx_d = 4763.87464;
% fy_d = 4763.87464;
% cx_d = 840;
% cy_d = 525;

  [xx,yy] = meshgrid(1:W, 1:H);
  X = (xx - cx_d) .* imgDepthAbs / fx_d;
  Y = (yy - cy_d) .* imgDepthAbs / fy_d;
  Z = imgDepthAbs;
  points3d = [X(:) Y(:) Z(:)];
%   删除背景点
  bg=find(points3d(:,3)==255);
  points3d(bg,:)=[];
  % 可视化
    plot3(points3d(:,1),points3d(:,2),points3d(:,3),'.','MarkerSize',2); 
    xlabel('X');
    ylabel('Y');
    zlabel('Z');
    hold on;
    axis equal;

% % %%************************************************************************
% %修改.obj保存路径
% filename_obj =('./0001.obj');  
% %filename_obj =[FindFiles, filename, '\model_2.obj'];  
% fid = fopen(filename_obj, 'w');  %打印头文件
% point=num2str(points3d);
% num=length(points3d);
% for row=1:num   %打印顶点
%     fprintf(fid, ['v ','%s\n'], point(row,:));
% end
% 
% fclose(fid);
end
