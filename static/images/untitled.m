Files=dir('*.jpeg');
opFolder=('/home/gandalf/Desktop/poster');
for k=1:length(Files)
   FileNames=Files(k).name;
   A = imread(FileNames);
   [x,y,z]=size(A);
   opFullFileName = fullfile(opFolder,FileNames)
   
   if(x>200 && y>200)
       imwrite(A,opFullFileName,'jpeg');
   end
end