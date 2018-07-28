import numpy as np
import cv2
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import pickle

def calibrate_camera():
	# Mapping each calibration image to number of checkerboard corners
	objp_dict = {
		1: (7, 7),
		2: (7, 7),
		3: (7, 7),
		4: (7, 7),
		5: (7, 7),
		6: (7, 7),
		7: (7, 7),
		8: (7, 7),
		9: (7, 7),
		10: (7, 7),
		11: (7, 7),
		12: (7, 7),
		13: (7, 7),
		14: (7, 7),
		15: (7, 7),
		16: (7, 7),
	}
	# List of object points and corners for calibration
	objp_list = []
	corners_list = []

	# Go through all images and find corners
	for k in objp_dict:
		nx, ny = objp_dict[k]

		# Prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
		objp = np.zeros((nx*ny,3), np.float32)
		objp[:,:2] = np.mgrid[0:nx, 0:ny].T.reshape(-1,2)

		# Make a list of calibration images
		fname = 'elp_camera_cal/calibration%s.jpg' % str(k)
		img = cv2.imread(fname)

		# Convert to grayscale
		gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

		# Find the chessboard corners
		ret, corners = cv2.findChessboardCorners(gray, (nx, ny), None)

		# If found, save & draw corners
		if ret == True:
			
			# Save object points and corresponding corners
			objp_list.append(objp)
			corners_list.append(corners)

			# Draw and display the corners
			cv2.drawChessboardCorners(img, (nx, ny), corners, ret)
			plt.figure(k)
			plt.imshow(img)
			plt.show()
			print('Found corners for %s' % fname)
			cv2.waitKey(0)
		else:
			print('Warning: ret = %s for %s' % (ret, fname))

	# Calibrate camera and undistort a test image
	img = cv2.imread('test_images/straight_lines1.jpg')
	img_size = (img.shape[1], img.shape[0])
	ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objp_list, corners_list, img_size,None,None)

	return mtx, dist

def main():
	mtx, dist = calibrate_camera()
	save_dict = {'mtx': mtx, 'dist': dist}
	with open('calibrate_camera.p', 'wb') as f:
		pickle.dump(save_dict, f, protocol=2)

if __name__ == '__main__':
	main()
