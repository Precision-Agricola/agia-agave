
def align_images(capture, index_red = 4,max_features = 500, keep_percentage = 0.2, debug=False):
    # Align image based on the detection and matching of feature points. ORB (Oriented Fast and Rotate BRIEF) detects coordinate of key points that are stable under image transformation (FAST locator) and describe the region around the points (BRISK descriptor).  
    # Input: capture (n x m x 5 np.array, double format), max_features (no. of candidate keypoint regions to consider), keep_percentage (Designates the percentage of keypoint matches to keep)
    # Output: transformed_image (n x m x 5 np.array, sint8 format)
    # https://www.pyimagesearch.com/2020/08/31/image-alignment-and-registration-with-opencv/

    Masked_8 = np.uint8(capture*255)            # Changes scale from float (0 to 1) to int (0 - 255)
    height, width = Masked_8[:,:,0].shape       # Find height and width of matriz 
    transformed_img = np.copy(Masked_8)         # Deep copy
    method = cv2.DESCRIPTOR_MATCHER_BRUTEFORCE_HAMMING
	
    for image in range(0,4): 
        # Find the keypoints and and extract binary local invariant features
        orb_detector = cv2.ORB_create(max_features)         # Initiate ORB detector, a keypoints detector.
        (kp1, d1) = orb_detector.detectAndCompute(transformed_img[:,:,image], None)           # Image to align
        (kp2, d2) = orb_detector.detectAndCompute(transformed_img[:,:,index_red], None)       # Reference image
        
        # Computes the distance between binary features to find the best matches. 
        matcher = cv2.DescriptorMatcher_create(method)
        matches = matcher.match(d1, d2)

        # Sort matches by their distance, (the small the distance, the more similar the features are). 
        matches = sorted(matches, key=lambda x:x.distance)

        # Remove bad matches (noise)
        matches = matches[:int(len(matches)*keep_percentage)]  
        
        if debug:
            matchedVis = cv2.drawMatches(image, kpsA, template, kpsB, matches, None)
            matchedVis = imutils.resize(matchedVis, width=1000)
            cv2.imshow("Matched Keypoints", matchedVis)
            cv2.waitKey(0)

        # Allocate memory for the keypoints (x, y)-coordinates from the top matches
        no_of_matches = len(matches)  
        p1 = np.zeros((no_of_matches, 2), dtype="float")  
        p2 = np.zeros((no_of_matches, 2), dtype="float") 

        # Extract location of good matches
        for i in range(len(matches)):
            # indicate that the two keypoints in the respective images map to each other 
            p1[i, :] = kp1[matches[i].queryIdx].pt  
            p2[i, :] = kp2[matches[i].trainIdx].pt
        
        # Compute the homography matrix between using the keypoints and RANSAC algorithm 
        homography, mask = cv2.findHomography(p1, p2, method=cv2.RANSAC)

        # Align by means of applying a warm perpective.
        transformed_img[:,:,image] = cv2.warpPerspective(transformed_img[:,:,image], homography, (width, height))
    if verbose: print(transformed_img)
    return transformed_img