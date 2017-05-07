import numpy as np
from sklearn.linear_model import LinearRegression


class LaneEval(object):
    lr = LinearRegression()
    thresh = 20

    @staticmethod
    def get_angle(xs, y_samples):
        # real_thresh = thresh / cos(theta)
        xs, ys = xs[xs >= 0], y_samples[xs > 0]
        LaneEval.lr.fit(ys[:, None], xs)
        k = LaneEval.lr.coef_[0]
        theta = np.arctan(k)
        return theta

    @staticmethod
    def line_accuracy(pred, gt, thresh):
        return np.sum(np.abs(pred - gt) < thresh, 1., 0.) / len(gt)

    @staticmethod
    def accuracy(pred, gt, y_samples):
        # pred = [x_preds]
        # gt = [x_gts]
        angles = [LaneEval.get_angle(x_gts, y_samples) for x_gts in gt]
        threshs = [LaneEval.thresh / np.cos(angle) for angle in angles]
        line_accs = []
        for x_gts, thresh in zip(pred, gt, threshs):
            accs = [LaneEval.line_accuracy(x_preds, x_gts, thresh) for x_preds in pred]
            line_accs.append(np.max(accs))
        return np.mean(line_accs)
