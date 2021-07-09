close all, clear all, clc; 

warning off;
%% read info
x1 = 5231; x2 = 6522;
y1 = 6007; y2 = 7370;
files = dir('data/idx*.tif');

for i = 1: size(files, 1)
 
    display(strcat('reading... ', files(i).name))
    all_canvas = imread(strcat('data/',files(i).name));   
    raw_images{i} = all_canvas(x1:x2,y1:y2);   
end
%%
red = raw_images{1}; green = raw_images{2}; blue = raw_images{3};
nir = raw_images{4}; edge = raw_images{5};

results = raw_images{6};
results(results==1)=0;

%% get index, results, and rgb data

[x, y] = size(red);

% make the rgb mask
rgb = cat(3, red,...
             green,...
             blue);

% get the results 
results_bin = results;
results_bin(results_bin == 1) = 0;
results_bin(results_bin < .89) = 0;
results_bin(results_bin >= .89) = 1;

%% region propperties

BW = im2bw(results,.4);
props = regionprops(BW, 'all');
area = 0; 
ndv = raw_images{6};
rgb = create_color_false(ndv, 0.2, 0.8,1) .* BW + rgb;
%% process only good info 

ndvi = results;
figure(1), imshow(BW)
Y = zeros(x, y);
hold on;
for i = 1: length(props)
    if props(i).Area > 10
        thisBB = props(i).BoundingBox;
        rectangle('Position',[thisBB(1),thisBB(2),thisBB(3),thisBB(4)],'EdgeColor','r','LineWidth',3);  
        
        % image base
        ndvi_base = ndvi(thisBB(2):thisBB(2) + thisBB(4) - 1, thisBB(1):thisBB(1) + thisBB(3) - 1) .* props(i).Image;
        
        % median
        regmaxs = imregionalmax(ordfilt2(ndvi_base,50,ones(10,10)),4);
        
        % local maximum
        Y(thisBB(2):thisBB(2) + thisBB(4) - 1, thisBB(1):thisBB(1) + thisBB(3) - 1) = regmaxs;
        

    area = area + props(i).Area;
    end
end
%%

N = logical(Y);
real_props = regionprops(N);
radio = zeros(1,length(real_props));

for i = 1: length(real_props)
    center_1 = floor(real_props(i).Centroid(1));
    center_2 = floor(real_props(i).Centroid(2));
    center_1_static = center_1;
    center_2_static = center_2;
    
    position   =[center_1 center_2];

    while(BW(center_2, center_1) ~= 0 && radio(i) < 100  && center_1 > 1 && center_2 > 1)
        radio(i) = radio(i) + 1;
        center_1 = center_1 - 1;
        center_2 = center_2 - 1; 
        
        if radio(i) <= 5
            rgb(center_2, center_1_static, 1) = 221/255;
            rgb(center_2, center_1_static, 2) = 91/255;
            rgb(center_2, center_1_static, 3) = 18/255;

        elseif (radio(i) > 6) && (radio(i) < 15)
            rgb(center_2, center_1_static, 1) = 180/255;
            rgb(center_2, center_1_static, 2) = 249/255;
            rgb(center_2, center_1_static, 3) = 165/255;

        else
            rgb(center_2, center_1_static, 1) = 66/2555;
            rgb(center_2, center_1_static, 2) = 104/255;
            rgb(center_2, center_1_static, 3) = 124/255;

        end
        
        if mod(i,20) == 0
        rgb = insertText(rgb, position,...
        strcat('Radio (cm): ', int2str(radio(i)*4.17)));
        end
                        
    end
end

figure(2)
imshow(rgb),title('results')

%%

%max(max(ndv))
figure(3);
imshow(create_color_false(ndv, 0.1, 0.9,1) .* BW + rgb);





