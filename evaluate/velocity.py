import numpy as np
import json


class VeloEval(object):

    @staticmethod
    def load_annotation(file_list):
        data_list = []
        for file_name in file_list:
            with open(file_name) as data_file:
                raw_data = json.load(data_file)
                data = []
                for instance in raw_data:
                    instance["bbox"] = np.array([[instance["bbox"]["top"],
                                                  instance["bbox"]["left"],
                                                  instance["bbox"]["bottom"],
                                                  instance["bbox"]["right"]]])
                    data.append(instance)
            data_list.append(data)
        print "Finished loading {0:d} annotations.".format(len(file_list))
        return data_list

    @staticmethod
    def calc_error(a, b):
        return np.linalg.norm(np.array(a)-np.array(b)) ** 2

    @staticmethod
    def get_distance_label(gt):
        distance = np.linalg.norm(np.array(gt["position"]))
        if distance < 15:
            return 0
        elif distance < 40:
            return 1
        else:
            return 2

    @staticmethod
    def find_nearest_gt(pred, x_gt):
        bboxes = np.vstack([x["bbox"] for x in x_gt])
        difference = np.sum(np.abs(np.subtract(bboxes, pred["bbox"])), axis=1)
        return x_gt[np.argmin(difference)]

    @staticmethod
    def accuracy(pred_list, gt_list):
        pos_error = [[], [], []]
        velo_error = [[], [], []]
        for x_pred, x_gt in zip(pred_list, gt_list):
            for pred in x_pred:
                gt = VeloEval.find_nearest_gt(pred, x_gt)
                distance_label = VeloEval.get_distance_label(gt)
                pos_error[distance_label].append(VeloEval.calc_error(pred["position"], gt["position"]))
                velo_error[distance_label].append(VeloEval.calc_error(pred["velocity"], gt["velocity"]))
        ve0 = np.mean(np.array(velo_error[0]))
        ve1 = np.mean(np.array(velo_error[1]))
        ve2 = np.mean(np.array(velo_error[2]))
        pe0 = np.mean(np.array(pos_error[0]))
        pe1 = np.mean(np.array(pos_error[1]))
        pe2 = np.mean(np.array(pos_error[2]))

        print "Velocity Estimation error (Near): {0:.5f}".format(ve0)
        print "Velocity Estimation error (Medium): {0:.5f}".format(ve1)
        print "Velocity Estimation error (Far): {0:.5f}".format(ve2)
        print "Velocity Estimation error total: {0: 5f}".format((ve0+ve1+ve2)/3)
        print "Position Estimation error (Near): {0:.5f}".format(pe0)
        print "Position Estimation error (Medium): {0:.5f}".format(pe1)
        print "Position Estimation error (Far): {0:.5f}".format(pe2)
        print "Position Estimation error total: {0:.5f}".format((pe0+pe1+pe2)/3)
        return (ve0+ve1+ve2)/3, (pe0+pe1+pe2)/3
