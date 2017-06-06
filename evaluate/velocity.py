import numpy as np
import json


class VeloEval(object):
    @staticmethod
    def load_json_file(file_list):
        data_list = []
        for file_name in file_list: 
            with open(file_name) as f:
                raw_data = json.load(f)
            data_list.append(raw_data)
        return data_list

    @staticmethod
    def transform_annotation(raw_data_list):
        anno_list = []
        for raw_data in raw_data_list:
            data = []
            for instance in raw_data:
                instance["bbox"] = np.array([[instance["bbox"]["top"],
                                              instance["bbox"]["left"],
                                              instance["bbox"]["bottom"],
                                              instance["bbox"]["right"]]])
                data.append(instance)
            anno_list.append(data)
        return anno_list                                  

    @staticmethod
    def load_annotation(file_list):
        raw_data_list = VeloEval.load_json_file(file_list)
        anno_list = VeloEval.transform_annotation(raw_data_list)
        print "Finished loading {0:d} annotations.".format(len(anno_list))
        return anno_list

    @staticmethod
    def calc_error(a, b):
        try:
            error = np.linalg.norm(np.array(a)-np.array(b)) ** 2
        except BaseException as e:
            raise Exception('Error data format')
        return np.linalg.norm(np.array(a)-np.array(b)) ** 2

    @staticmethod
    def get_distance_label(gt):
        distance = np.linalg.norm(np.array(gt["position"]))
        if distance < 20:
            return 0
        elif distance < 45:
            return 1
        else:
            return 2

    @staticmethod
    def find_nearest_gt(pred, x_gt):
        bboxes = np.vstack([x["bbox"] for x in x_gt])
        difference = np.sum(np.abs(np.subtract(bboxes, pred["bbox"])), axis=1)
        if np.min(difference) > 5:
            raise Exception('We do not get all the predictions for a certain frame')
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
    
    @staticmethod
    def bench_one_submit(pred_file, gt_file):
        try:
            with open(pred_file, 'r') as f:
                json_pred = json.load(f)
            with open(gt_file, 'r') as f:
                json_gt = json.load(f)    
        except BaseException as e:
            raise Exception('Fail to load json file of the prediction.')
        if len(json_gt) != len(json_pred):
            raise Exception('We do not get the predictions of all the test tasks')
        pred_list = VeloEval.transform_annotation(json_pred)
        gt_list = VeloEval.transform_annotation(json_gt)
        pos_error = [[], [], []]
        velo_error = [[], [], []]
        for x_pred, x_gt in zip(pred_list, gt_list):
            for gt in x_gt:
                pred = VeloEval.find_nearest_gt(gt, x_pred)
                distance_label = VeloEval.get_distance_label(gt)
                if 'position' not in pred or 'velocity' not in pred:
                    raise Exception('Missing position or velocity')
                pos_error[distance_label].append(VeloEval.calc_error(pred["position"], gt["position"]))
                velo_error[distance_label].append(VeloEval.calc_error(pred["velocity"], gt["velocity"]))
        
        ve0 = np.mean(np.array(velo_error[0]))
        ve1 = np.mean(np.array(velo_error[1]))
        ve2 = np.mean(np.array(velo_error[2]))
        pe0 = np.mean(np.array(pos_error[0]))
        pe1 = np.mean(np.array(pos_error[1]))
        pe2 = np.mean(np.array(pos_error[2]))

        return json.dumps({'VE':(ve0+ve1+ve2)/3, 'VENear':ve0, 'VEMed':ve1, 'VEFar':ve2, 'PE':(pe0+pe1+pe2)/3, 'PENear':pe0, 'PEMed':pe1, 'PEFar':pe2})
