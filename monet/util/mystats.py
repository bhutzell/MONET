from __future__ import division
from __future__ import print_function
from builtins import str
from past.utils import old_div
import numpy as np
from pandas import DataFrame, crosstab


def STDO(obs, mod, axis=None):
    """ Standard deviation of Observations """
    return np.ma.std(obs, axis=axis)


def STDP(obs, mod, axis=None):
    """ Standard deviation of Predictions """
    return np.ma.std(mod, axis=axis)


def MNB(obs, mod, axis=None):
    """ Mean Normalized Bias (%)"""
    return np.ma.masked_invalid(old_div(
        (mod - obs), obs)).mean(axis=axis) * 100.



def MNE(obs, mod, axis=None):
    """ Mean Normalized Gross Error (%)"""
    return np.ma.masked_invalid(old_div(np.ma.abs(mod - obs),
                                        obs)).mean(axis=axis) * 100.

def MdnNB(obs, mod, axis=None):
    """ Median Normalized Bias (%)"""
    return np.ma.median(
        np.ma.masked_invalid(old_div((mod - obs), obs)), axis=axis) * 100.

def MdnNE(obs, mod, axis=None):
    """ Median Normalized Gross Error (%)"""
    return np.ma.median(
        np.ma.masked_invalid(old_div(np.ma.abs(mod - obs), obs)),
        axis=axis) * 100.


def NMdnGE(obs, mod, axis=None):
    """ Normalized Median Gross Error (%)"""
    return np.ma.masked_invalid(
        old_div(np.ma.abs(mod - obs).mean(axis=axis),
                obs.mean(axis=axis))) * 100.


def NO(obs, mod, axis=None):
    """ N Observations (#)"""
    return (np.ma.getmaskarray(obs) == False).sum(axis=axis)


def NOP(obs, mod, axis=None):
    """ N Observations/Prediction Pairs (#)"""
    obsc, modc = matchmasks(obs, mod)
    return (np.ma.getmaskarray(obsc) == False).sum(axis=axis)


def NP(obs, mod, axis=None):
    """ N Predictions (#)"""
    return (np.ma.getmaskarray(mod) == False).sum(axis=axis)


def MO(obs, mod, axis=None):
    """ Mean Observations (obs unit)"""
    return obs.mean(axis=axis)


def MP(obs, mod, axis=None):
    """ Mean Predictions (model unit)"""
    return mod.mean(axis=axis)


def MdnO(obs, mod, axis=None):
    """ Median Observations (obs unit)"""
    return np.ma.median(obs, axis=axis)


def MdnP(obs, mod, axis=None):
    """ Median Predictions (model unit)"""
    return np.ma.median(mod, axis=axis)


def RM(obs, mod, axis=None):
    """ Mean Ratio Observations/Predictions (none)"""
    return np.ma.masked_invalid(old_div(obs, mod)).mean(axis=axis)


def RMdn(obs, mod, axis=None):
    """ Median Ratio Observations/Predictions (none)"""
    return np.ma.median(np.ma.masked_invalid(old_div(obs, mod)), axis=axis)


def MB(obs, mod, axis=None):
    """ Mean Bias"""
    return (mod - obs).mean(axis=axis)


def MdnB(obs, mod, axis=None):
    """ Median Bias"""
    return np.ma.median(mod - obs, axis=axis)


def WDMB(obs, mod, axis=None):
    """ Wind Direction Mean Bias"""
    return circlebias(mod - obs).mean(axis=axis)


def WDMdnB(obs, mod, axis=None):
    """ Wind Direction Median Bias"""
    return np.ma.median(circlebias(mod - obs), axis=axis)


def NMB(obs, mod, axis=None):
    """ Normalized Mean Bias (%)"""
    return (mod - obs).sum(axis=axis) / obs.sum(axis=axis) * 100.


def NMdnB(obs, mod, axis=None):
    """ Normalized Median Bias (%)"""
    return np.ma.median(
        mod - obs, axis=axis) / np.ma.median(
            obs, axis=axis) * 100.


def FB(obs, mod, axis=None):
    """ Fractional Bias (%)"""
    return ((np.ma.masked_invalid(old_div(
        (mod - obs), (mod + obs)))).mean(axis=axis) * 2.) * 100.


def ME(obs, mod, axis=None):
    """ Mean Gross Error (model and obs unit)"""
    return np.ma.abs(mod - obs).mean(axis=axis)


def MdnE(obs, mod, axis=None):
    """ Median Gross Error (model and obs unit)"""
    return np.ma.median(np.ma.abs(mod - obs), axis=axis)


def WDME(obs, mod, axis=None):
    """ Wind Direction Mean Gross Error (model and obs unit)"""
    return np.ma.abs(circlebias(mod - obs)).mean(axis=axis)


def WDMdnE(obs, mod, axis=None):
    """ Wind Direction Median Gross Error (model and obs unit)"""
    cb = circlebias(mod - obs)
    return np.ma.median(np.ma.abs(cb), axis=axis)


def NME(obs, mod, axis=None):
    """ Normalized Mean Error (%)"""
    out = (old_div(np.ma.abs(mod - obs).sum(axis=axis),
                   obs.sum(axis=axis))) * 100
    return out


def NMdnE(obs, mod, axis=None):
    """ Normalized Median Error (%)"""
    out = np.ma.median(
        np.ma.abs(mod - obs), axis=axis) / np.ma.median(
            obs, axis=axis) * 100
    return out


def FE(obs, mod, axis=None):
    """ Fractional Error (%)"""
    return (old_div(np.ma.abs(mod - obs),
                    (mod + obs))).mean(axis=axis) * 2. * 100.


def USUTPB(obs, mod, axis=None):
    """ Unpaired Space/Unpaired Time Peak Bias (%)"""
    return (old_div(
        (mod.max(axis=axis) - obs.max(axis=axis)), obs.max(axis=axis))) * 100.


def USUTPE(obs, mod, axis=None):
    """ Unpaired Space/Unpaired Time Peak Error (%)"""
    return (old_div(
        np.ma.abs(mod.max(axis=axis) - obs.max(axis=axis)),
        obs.max(axis=axis))) * 100.


def MNPB(obs, mod, paxis, axis=None):
    """ Mean Normalized Peak Bias (%)"""
    return (old_div(
        (mod.max(axis=paxis) - obs.max(axis=paxis)),
        obs.max(axis=paxis))).mean(axis=axis) * 100.


def MdnNPB(obs, mod, paxis, axis=None):
    """ Median Normalized Peak Bias (%)"""
    return np.ma.median(
        old_div(
            (mod.max(axis=paxis) - obs.max(axis=paxis)), obs.max(axis=paxis)),
        axis=axis) * 100.


def MNPE(obs, mod, paxis, axis=None):
    """ Mean Normalized Peak Error (%)"""
    return (old_div(
        (np.ma.abs(mod.max(axis=paxis) - obs.max(axis=paxis))),
        obs.max(axis=paxis))).mean(axis=axis) * 100.

def MdnNPE(obs, mod, paxis, axis=None):
    """ Median Normalized Peak Bias (%)"""
    return np.ma.median(
        old_div(
            (np.ma.abs(mod.max(axis=paxis) - obs.max(axis=paxis))),
            obs.max(axis=paxis)),
        axis=axis) * 100.


def NMPB(obs, mod, paxis, axis=None):
    """ Normalized Mean Peak Bias (%)"""
    return (mod.max(axis=paxis) - obs.max(axis=paxis)
            ).mean(axis=axis) / obs.max(axis=paxis).mean(axis=axis) * 100.


def NMdnPB(obs, mod, paxis, axis=None):
    """ Normalized Median Peak Bias (%)"""
    return np.ma.median(
        (mod.max(axis=paxis) - obs.max(axis=paxis)), axis=axis) / np.ma.median(
            obs.max(axis=paxis), axis=axis) * 100.


def NMPE(obs, mod, paxis, axis=None):
    """ Normalized Mean Peak Error (%)"""
    return (np.ma.abs(mod.max(axis=paxis) - obs.max(axis=paxis))
            ).mean(axis=axis) / obs.max(axis=paxis).mean(axis=axis) * 100.


def NMdnPE(obs, mod, paxis, axis=None):
    """ Normalized Median Peak Bias (%)"""
    return np.ma.median(
        np.ma.abs(mod.max(axis=paxis) - obs.max(axis=paxis)),
        axis=axis) / np.ma.median(
            obs.max(axis=paxis), axis=axis) * 100.


def PSUTMNPB(obs, mod, axis=None):
    """ Paired Space/Unpaired Time Mean Normalized Peak Bias (%)"""
    return MNPB(obs, mod, paxis=0, axis=None)


def PSUTMdnNPB(obs, mod, axis=None):
    """ Paired Space/Unpaired Time Median Normalized Peak Bias (%)"""
    return MdnNPB(obs, mod, paxis=0, axis=None)


def PSUTMNPE(obs, mod, axis=None):
    """ Paired Space/Unpaired Time Mean Normalized Peak Error (%)"""
    return MNPE(obs, mod, paxis=0, axis=None)


def PSUTMdnNPE(obs, mod, axis=None):
    """ Paired Space/Unpaired Time Median Normalized Peak Error (%)"""
    return MdnNPE(obs, mod, paxis=0, axis=None)


def PSUTNMPB(obs, mod, axis=None):
    """ Paired Space/Unpaired Time Normalized Mean Peak Bias (%)"""
    return NMPB(obs, mod, paxis=0, axis=None)


def PSUTNMPE(obs, mod, axis=None):
    """ Paired Space/Unpaired Time Normalized Mean Peak Error (%)"""
    return NMPE(obs, mod, paxis=0, axis=None)


def PSUTNMdnPB(obs, mod, axis=None):
    """ Paired Space/Unpaired Time Normalized Median Peak Bias (%)"""
    return NMdnPB(obs, mod, paxis=0, axis=None)


def PSUTNMdnPE(obs, mod, axis=None):
    """ Paired Space/Unpaired Time Normalized Median Peak Error (%)"""
    return NMdnPE(obs, mod, paxis=0, axis=None)


def R2(obs, mod, axis=None):
    """ Coefficient of Determination (unit squared)"""
    from scipy.stats import pearsonr
    if axis is None:
        obsc, modc = matchedcompressed(obs, mod)
        return pearsonr(obsc, modc)[0]**2
    else:
        raise ValueError('Not ready yet')


def RMSE(obs, mod, axis=None):
    """ Root Mean Square Error (model unit)"""
    return np.ma.sqrt(((mod - obs)**2).mean(axis=axis))


def WDRMSE(obs, mod, axis=None):
    """ Wind Direction Root Mean Square Error (model unit)"""
    return np.ma.sqrt(((circlebias(mod - obs))**2).mean(axis=axis))


def RMSEs(obs, mod, axis=None):
    """Root Mean Squared Error (obs, mod_hat)"""
    if axis is None:
        try:
            from scipy.stats import linregress
            obsc, modc = matchedcompressed(obs, mod)
            m, b, rval, pval, stderr = linregress(obsc, modc)
            mod_hat = b + m * obs
            return RMSE(obs, mod_hat)
        except ValueError:
            return None
    else:
        raise ValueError('Not ready yet')


def matchmasks(a1, a2):
    mask = np.ma.getmaskarray(a1) | np.ma.getmaskarray(a2)
    return np.ma.masked_where(mask, a1), np.ma.masked_where(mask, a2)


def matchedcompressed(a1, a2):
    a1, a2 = matchmasks(a1, a2)
    return a1.compressed(), a2.compressed()


def RMSEu(obs, mod, axis=None):
    """Root Mean Squared Error (mod_hat, mod)"""
    if axis is None:
        try:
            from scipy.stats import linregress
            obsc, modc = matchedcompressed(obs, mod)
            m, b, rval, pval, stderr = linregress(obsc, modc)
            mod_hat = b + m * obs
            return RMSE(mod_hat, mod)
        except ValueError:
            return None
    else:
        raise ValueError('Not ready yet')


def d1(obs, mod, axis=None):
    """ Modified Index of Agreement, d1"""
    return 1.0 - old_div(
        (np.ma.abs(obs - mod)).sum(axis=axis),
        (np.ma.abs(mod - obs.mean(axis=axis)) +
         np.ma.abs(obs - obs.mean(axis=axis))).sum(axis=axis))


def E1(obs, mod, axis=None):
    """ Modified Coefficient of Efficiency, E1"""
    return 1.0 - old_div(
        (np.ma.abs(obs - mod)).sum(axis=axis),
        (np.ma.abs(obs - obs.mean(axis=axis))).sum(axis=axis))


def IOA(obs, mod, axis=None):
    """ Index of Agreement, IOA"""
    obsmean = obs.mean(axis=axis)
    if not axis is None:
        obsmean = np.expand_dims(obsmean, axis=axis)
    return 1.0 - old_div(
        (np.ma.abs(obs - mod)**2).sum(axis=axis),
        ((np.ma.abs(mod - obsmean) + np.ma.abs(obs - obsmean)) **
         2).sum(axis=axis))


def circlebias(b):
    b = np.ma.where(b > 180, b - 360, b)
    b = np.ma.where(b < -180, b + 360, b)
    return b


def WDIOA(obs, mod, axis=None):
    """ Wind Direction Index of Agreement, IOA"""
    obsmean = obs.mean(axis=axis)
    if not axis is None:
        obsmean = np.expand_dims(obsmean, axis=axis)
    b = circlebias(mod - obs)

    bhat = circlebias(mod - obsmean)

    ohat = circlebias(obs - obsmean)

    return 1.0 - old_div(
        (np.ma.abs(b)**2).sum(axis=axis),
        ((np.ma.abs(bhat) + np.ma.abs(ohat))**2).sum(axis=axis))


def AC(obs, mod, axis=None):
    """ Anomaly Correlation """
    obs_bar = obs.mean(axis=axis)
    if not axis is None:
        obs_bar = np.expand_dims(obs_bar, axis=axis)
    p1 = ((mod - obs_bar) * (obs - obs_bar)).sum(axis=axis)
    p2 = (((mod - obs_bar)**2).sum(axis=axis) * (
        (obs - obs_bar)**2).sum(axis=axis))**0.5
    return old_div(p1, p2)


def WDAC(obs, mod, axis=None):
    """ Wind Direction Anomaly Correlation """
    obs_bar = obs.mean(axis=axis)
    if not axis is None:
        obs_bar = np.expand_dims(obs_bar, axis=axis)
    p1 = (circlebias(mod - obs_bar) * circlebias(obs - obs_bar)).sum(axis=axis)
    p2 = ((circlebias(mod - obs_bar)**2).sum(axis=axis) *
          (circlebias(obs - obs_bar)**2).sum(axis=axis))**0.5
    return old_div(p1, p2)


def HSS(obs, mod, minval, maxval):
    """
    Heidke Skill Score (1 is perfect - below zero means no confidence)
    :param obs:
    :param mod:
    :param minval:
    :param maxval:
    :return: HSS
    """
    a, b, c, d = scores(obs, mod, minval, maxval=maxval)
    hss = 2 * (a * d - b * c) / ((a + c) * (c + d) + (a + b) * (b + d))
    print('HSS for range ' + str(minval) + ' --> ' + str(maxval) + ': ' + hss)
    return hss


def ETS(obs, mod, minval, maxval):
    """
    Equitable Threat Score (1 is perfect - Range -1/3 -> 1)
    :param obs:
    :param mod:
    :param minval:
    :param maxval:
    :return: HSS
    """
    a, b, c, d = scores(obs, mod, minval, maxval=maxval)
    ar = (a + b) * (a + c) / (a + b + c + d)
    ets = old_div((a - ar), (a + b + c - ar))
    print('ETS for range ' + str(minval) + ' --> ' + str(maxval) + ': ' + ets)
    return ets


def scores(obs, mod, minval, maxval=1.0e5):
    d = {}
    d['obs'] = obs
    d['mod'] = mod
    df = DataFrame(d)
    ct = crosstab(
        (df['mod'] > minval) & (df['mod'] < maxval),
        (df['obs'] > minval) & (df['obs'] < maxval),
        margins=True)
    #    print ct
    a = ct[1][1].astype('float')
    b = ct[1][0].astype('float')
    c = ct[0][1].astype('float')
    d = ct[0][0].astype('float')
    return a, b, c, d


def stats(df, minval, maxval):
    from numpy import sqrt
    dd = {}
    dd['N'] = df.Obs.dropna().count()
    dd['Obs'] = df.Obs.mean()
    dd['Mod'] = df.CMAQ.mean()
    dd['MB'] = MB(df.Obs.values, df.CMAQ.values)  # mean bias
    dd['R'] = sqrt(R2(df.Obs.values, df.CMAQ.values))  # pearsonr ** 2
    dd['IOA'] = IOA(df.Obs.values, df.CMAQ.values)  # Index of Agreement
    dd['RMSE'] = RMSE(df.Obs.values, df.CMAQ.values)
    dd['NMB'] = NMB(df.Obs.values, df.CMAQ.values)
    try:
        a, b, c, d = scores(df.Obs.values, df.CMAQ.values, 70, 1000)
        dd['POD'] = old_div(a, (a + b))
        dd['FAR'] = old_div(c, (a + c))
    except:
        dd['POD'] = 1.
        dd['FAR'] = 0.
    return dd
