import random
import time
import cv2
import numpy as np
import math

class SingleCovidSimulator:
    def __init__(self, rVals=(1.1, 1.4)):
        self.rVals = rVals
        self.width = 400
        self.height = 500
        self.w_margin = 4
        self.label_h = 100
        self.l_start = self.w_margin
        self.l_end = int(self.width / 2 - self.w_margin / 2)
        self.last = time.perf_counter()
        self.r_start = int(self.width / 2 + self.w_margin / 2)
        self.r_end = self.width - self.w_margin
        self.day_num = 0
        self.rad = 3
        self.currentPoints = []
        self.initVals()
        self.bg = 255 * np.ones((self.height, self.width, 3), np.uint8)
        self.bg = self.addPoints(self.bg)
    def initVals(self):
        self.day_num = 0
        startingPointsLeft = [
            [random.randrange(self.l_start, self.l_end), random.randrange(self.label_h, self.height), 0, 'left',
             self.rVals[0]] for
            _ in range(5)]
        startingPointsRight = [
            [random.randrange(self.r_start, self.r_end), random.randrange(self.label_h, self.height), 0, 'right', self.rVals[1]]
            for _ in range(5)]
        startingPoints = startingPointsLeft + startingPointsRight
        self.currentPoints = startingPoints

    def update(self):
        new_time = time.perf_counter()
        if new_time - self.last > 0.25:
            self.initVals()
            self.last = time.perf_counter()
            return
        else:
            time.sleep(0.25 - new_time + self.last)
            self.last = time.perf_counter()
            self.bg = self.nextRound()
            return

    def read(self):
        return self.bg

    def getNewPoints(self):
        newPoints = []
        for point in self.currentPoints:
            if point[2] < 15 and random.randrange(0, 140) < point[4]*10:
                newPoints.append(self.createPoint(point))
            point[2] += 1
        self.currentPoints += newPoints
    def addPoints(self, frame):
        up_frame = frame
        for point in self.currentPoints:
            if point[2] <= 14:
                pt = (point[0], point[1])
                up_frame = cv2.circle(up_frame, pt, self.rad, (int((min(point[2], 14)) / 14 * 255), int((min(point[2], 14)) / 14 * 255), 255), -1)
                # up_frame = cv2.circle(up_frame, pt, self.rad, (0, 0, 0), 1)
        font = cv2.FONT_HERSHEY_SIMPLEX
        left_size = cv2.getTextSize('R = 1.1', font, 1, 2)[0]
        right_size = cv2.getTextSize('R = 1.4', font, 1, 2)[0]
        days_counter_size = cv2.getTextSize(f"Day {self.day_num}", font, 1, 2)[0]
        left_text_coord = (int((self.l_end - self.l_start - left_size[0]) / 2 + self.l_start), int(self.label_h * 3 / 4))
        right_text_coord = (int((self.r_end - self.r_start - right_size[0]) / 2) + self.r_start, int(self.label_h * 3 / 4))
        days_counter_coord = (int((self.width - days_counter_size[0]) / 2), int(self.label_h / 4))
        up_frame = cv2.putText(up_frame, 'R = 1.1', left_text_coord, font, 1, (0, 0, 0), 2, cv2.LINE_AA)
        up_frame = cv2.putText(up_frame, 'R = 1.4', right_text_coord, font, 1, (0, 0, 0), 2, cv2.LINE_AA)
        up_frame = cv2.putText(up_frame, f"Day {self.day_num}", days_counter_coord, font, 1, (0, 0, 0), 2, cv2.LINE_AA)

        start_rect = (self.l_end, self.label_h)
        end_rect = (self.r_start, self.height)
        black = (0, 0, 0)
        up_frame = cv2.rectangle(up_frame, start_rect, end_rect, black, -1)
        return up_frame
    def nextRound(self):
        frame = 255 * np.ones((self.height, self.width, 3), np.uint8)
        frame = self.addPoints(frame)
        self.getNewPoints()
        self.day_num += 1
        return frame
    def createPoint(self, point):
        offset_theta = random.uniform(0, 2*math.pi)
        offset_r = random.uniform(self.rad, 8*self.rad)
        gen_point = [int(point[0] + offset_r * math.cos(offset_theta)), int(point[1] + offset_r * math.sin(offset_theta)), 0, point[3], point[4]]
        if ((gen_point[3] == 'left' and (self.l_start < gen_point[0] < self.l_end)) or (gen_point[3] == 'right' and (self.r_start < gen_point[0] < self.r_end))) and (self.label_h < gen_point[1] < self.height):
            # print(f"succeeded, with point {gen_point}, and starting point {point}")
            return gen_point
        # print(f"failed, with point {gen_point}, and starting point {point}")
        return self.createPoint(point)