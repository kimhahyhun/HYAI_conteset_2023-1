import cv2
import numpy as np


def trans(img):
    img_ori = img
    # img_ori = cv2.flip(img_ori, 1)

    hsvim = cv2.cvtColor(img_ori, cv2.COLOR_BGR2HSV)
    lower = np.array([0, 25, 75], dtype="uint8")
    upper = np.array([100, 175, 200], dtype="uint8")
    skinRegionHSV = cv2.inRange(hsvim, lower, upper)
    blurred = cv2.blur(skinRegionHSV, (10, 10), 0)
    # gray_img = cv2.cvtColor(blurred, cv2.COLOR_RGB2GRAY)
    ret, thresh = cv2.threshold(blurred, 175, 255, cv2.THRESH_BINARY)
    # thresh = hsvim

    # thresh = img

    # cv2.imshow('aa',hsvim)
    # # cv2.imshow('skinRegionHSV')
    # cv2.imshow('blu',blurred)
    # # cv2.imshow('iaa', thresh)
    # cv2.waitKey()
    # cv2.destroyAllWindows()

    contours, hierarchy = cv2.findContours(
        thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    contours_dict = []

    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        contours_dict.append({
            'contour': contour,
            'x': x,
            'y': y,
            'w': w,
            'h': h,
            'cx': x + (w / 2),
            'cy': y + (h / 2)
        })

    MIN_AREA = 10000
    MAX_AREA = 50000
    MIN_WIDTH, MIN_HEIGHT = 0, 0
    MIN_RATIO, MAX_RATIO = 0.2, 10.1

    # MIN_AREA = 0
    # MIN_WIDTH, MIN_HEIGHT = 0, 0
    # MIN_RATIO, MAX_RATIO = 0, 10000000000000000

    possible_contours = []

    sum_height = 0
    sum_width = 0

    cnt = 0
    for d in contours_dict:
        area = d['w'] * d['h']
        ratio = d['w'] / d['h']

        sum_width += d['w']
        sum_height += d['h']
        # possible contours
        if MAX_AREA > area > MIN_AREA and d['w'] > MIN_WIDTH and d['h'] > MIN_HEIGHT and MIN_RATIO < ratio < MAX_RATIO:
            d['idx'] = cnt
            cnt += 1
            possible_contours.append(d)

    dst1 = copy.copy(img)
    dst2 = copy.copy(img)

    for d in possible_contours:
        cv2.drawContours(dst1, d['contour'], -1, (255, 255, 0), 5)
        cv2.rectangle(dst1, pt1=(d['x'], d['y']), pt2=(d['x'] + d['w'], d['y'] + d['h']), color=(255, 255, 255),
                      thickness=2)
    for d in contours_dict:
        cv2.drawContours(dst2, d['contour'], -1, (255, 255, 0), 5)
        cv2.rectangle(dst2, pt1=(d['x'], d['y']), pt2=(d['x'] + d['w'], d['y'] + d['h']), color=(255, 255, 255),
                      thickness=2)

    # if contact(possible_contours):
    #    make_stain(img_ori)

    # img_ori = cv2.circle(img_ori, (stain_point[0], stain_point[1]), 50, (255, 255, 0), -1)
    # cv2.putText(img_ori, f"scord : {score}", (1, 13 * 2), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2, cv2.LINE_AA)
    # dst2 = cv2.resize(img_ori, (0, 0), fx=1.0, fy=1.0, interpolation=cv2.INTER_LINEAR)

    crop_images = []

    for d in possible_contours:
        # cv2.drawContours(dst1, d['contour'], -1, (255, 255, 0), 5)
        cv2.rectangle(dst1, pt1=(d['x'], d['y']), pt2=(d['x'] + d['w'], d['y'] + d['h']), color=(255, 255, 255),
                      thickness=2)
        x_start = d['x'] - 40
        y_start = d['y'] - 40
        x_finish = d['x'] + d['w'] + 40
        y_finish = d['y'] + d['h'] + 40

        crop_img = img[y_start:y_finish, x_start:x_finish]
        crop_images.append(crop_img)

    # cv2.imshow('11', dst1)
    # cv2.imshow('22',dst2)
    # cv2.waitKey()
    # cv2.destroyAllWindows()

    return crop_images
