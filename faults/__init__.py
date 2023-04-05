import pandas as pd
import pandas.api.types as pdtypes


class HelperUtils():
    def float_check_err(self, col):
        err_str = " column failed with a check that the data is a float"
        return str(col) + err_str

    def float_max_check_err(self, col):
        err_str = " column failed with a check that the data is a float between 0.0 and 1.0"
        return str(col) + err_str

    def int_check_err(self, col):
        err_str = " column failed with a check that the data is type int"
        return str(col) + err_str

    def int_max_check_err(self, col):
        err_str = " column failed with a check that the status data for a motor or isolation valve is an int between 0 and 1"
        return str(col) + err_str

    def isfloat(self, num):
        try:
            float(num)
            return True
        except:
            return False

    def isLessThanOnePointOne(self, num):
        try:
            if num <= 1.0:
                return True
        except:
            return False


class FaultConditionOne:
    """OS1 - Diff pressure too high with pumps off"""

    def __init__(
        self,
        pump_diff_press_err_thres: float,
        pump_diff_press_col: str,
        pump_status_bool_col: str,
        pump_diff_press_setpoint_col: str,
        troubleshoot=False
    ):
        self.pump_diff_press_err_thres = pump_diff_press_err_thres
        self.pump_diff_press_col = pump_diff_press_col
        self.pump_status_bool_col = pump_status_bool_col
        self.pump_diff_press_setpoint_col = pump_diff_press_setpoint_col
        self.troubleshoot = troubleshoot

    def apply(self, df: pd.DataFrame) -> pd.DataFrame:

        # check analog ouputs [data with units of %] are floats only
        for col in [
            self.pump_vfd_speed_col
        ]:
            if not pdtypes.is_float_dtype(df[col]):
                raise TypeError(HelperUtils().float_check_err(col))

            if df[col].max() > 1.0:
                raise TypeError(HelperUtils().float_max_check_err(col))

        df['pump_diff_press_check'] = (
            df[self.pump_diff_press_col] < df[self.pump_diff_press_setpoint_col] - self.pump_diff_press_err_thres)

        df['pump_check'] = df[self.pump_status_bool_col] == 0

        df["fc1_flag"] = (df['pump_diff_press_check'] &
                          df['pump_check']).astype(int)

        if self.troubleshoot:
            print("Troubleshoot mode enabled - not removing helper columns")

        else:
            del df['pump_diff_press_check']
            del df['pump_check']

        return df


class FaultConditionTwo:
    """OS1 - Flow meter when PRIMARY pumps are off should be zero"""

    def __init__(
        self,
        flow_meter_err_thres: float,
        flow_meter_col: str,
        pump_status_bool_col: str,
        troubleshoot=False
    ):
        self.flow_meter_err_thres = flow_meter_err_thres
        self.flow_meter_col = flow_meter_col
        self.pump_status_bool_col = pump_status_bool_col
        self.troubleshoot = troubleshoot

    def apply(self, df: pd.DataFrame) -> pd.DataFrame:

        # check if motor status is an int only
        for col in [
            self.pump_status_bool_col
        ]:
            if not pdtypes.is_integer_dtype(df[col]):
                raise TypeError(HelperUtils().int_check_err(col))

            if df[col].max() > 1:
                raise TypeError(HelperUtils().int_max_check_err(col))

        df['flow_meter_check'] = df[self.flow_meter_col] > self.flow_meter_err_thres

        df['pump_check'] = df[self.pump_status_bool_col] == 0

        df["fc2_flag"] = (df['flow_meter_check'] &
                          df['pump_check']).astype(int)

        if self.troubleshoot:
            print("Troubleshoot mode enabled - not removing helper columns")

        else:
            del df['flow_meter_check']
            del df['pump_check']

        return df


class FaultConditionThree:
    """OS1 - Flow meter when SECONDARY pumps are off should be zero"""

    def __init__(
        self,
        flow_meter_err_thres: float,
        flow_meter_col: str,
        pump_status_bool_col: str,
        troubleshoot=False
    ):
        self.flow_meter_err_thres = flow_meter_err_thres
        self.flow_meter_col = flow_meter_col
        self.pump_status_bool_col = pump_status_bool_col
        self.troubleshoot = troubleshoot

    def apply(self, df: pd.DataFrame) -> pd.DataFrame:

        # check if motor status is an int only
        for col in [
            self.pump_status_bool_col
        ]:
            if not pdtypes.is_integer_dtype(df[col]):
                raise TypeError(HelperUtils().int_check_err(col))

            if df[col].max() > 1:
                raise TypeError(HelperUtils().int_max_check_err(col))

        df['flow_meter_check'] = df[self.flow_meter_col] > self.flow_meter_err_thres

        df['pump_check'] = df[self.pump_status_bool_col] == 0

        df["fc3_flag"] = (df['flow_meter_check'] &
                          df['pump_check']).astype(int)

        if self.troubleshoot:
            print("Troubleshoot mode enabled - not removing helper columns")

        else:
            del df['flow_meter_check']
            del df['pump_check']

        return df


class FaultConditionFour:
    """OS2,3 - Pumps not making DP setpoint"""

    def __init__(
        self,
        vfd_speed_percent_err_thres: float,
        vfd_speed_percent_max: float,
        pump_diff_press_err_thres: float,
        pump_diff_press_col: str,
        pump_vfd_speed_col: str,
        pump_diff_press_setpoint_col: str,
        troubleshoot=False
    ):
        self.vfd_speed_percent_err_thres = vfd_speed_percent_err_thres
        self.vfd_speed_percent_max = vfd_speed_percent_max
        self.pump_diff_press_err_thres = pump_diff_press_err_thres
        self.pump_diff_press_col = pump_diff_press_col
        self.pump_vfd_speed_col = pump_vfd_speed_col
        self.pump_diff_press_setpoint_col = pump_diff_press_setpoint_col
        self.troubleshoot = troubleshoot

    def apply(self, df: pd.DataFrame) -> pd.DataFrame:

        # check analog ouputs [data with units of %] are floats only
        for col in [
            self.pump_vfd_speed_col
        ]:
            if not pdtypes.is_float_dtype(df[col]):
                raise TypeError(HelperUtils().float_check_err(col))

            if df[col].max() > 1.0:
                raise TypeError(HelperUtils().float_max_check_err(col))

        df['pump_diff_press_check'] = (
            df[self.pump_diff_press_col] < df[self.pump_diff_press_setpoint_col] - self.pump_diff_press_err_thres)
        df['pump_check'] = (df[self.pump_vfd_speed_col] >=
                            self.vfd_speed_percent_max - self.vfd_speed_percent_err_thres)

        df["fc4_flag"] = (df['pump_diff_press_check'] &
                          df['pump_check']).astype(int)

        if self.troubleshoot:
            print("Troubleshoot mode enabled - not removing helper columns")

        else:
            del df['pump_diff_press_check']
            del df['pump_check']

        return df


class FaultConditionFive:
    """OS2,3 - Flow meter when SECONDARY pumps are off should be zero"""

    def __init__(
        self,
        flow_meter_err_thres: float,
        hot_water_min_flow_stp: float,
        hot_water_bypass_vlv_err_thres: float,
        flow_meter_col: str,
        hot_water_bypass_vlv_cmd_col: str,
        pump_status_bool_col: str,
        troubleshoot=False
    ):
        self.flow_meter_err_thres = flow_meter_err_thres
        self.hot_water_min_flow_stp = hot_water_min_flow_stp
        self.hot_water_bypass_vlv_err_thres = hot_water_bypass_vlv_err_thres
        self.flow_meter_col = flow_meter_col
        self.hot_water_bypass_vlv_cmd_col = hot_water_bypass_vlv_cmd_col
        self.pump_status_bool_col = pump_status_bool_col
        self.troubleshoot = troubleshoot

    def apply(self, df: pd.DataFrame) -> pd.DataFrame:

        # check if motor status bool point is an int only
        for col in [
            self.pump_status_bool_col
        ]:
            if not pdtypes.is_integer_dtype(df[col]):
                raise TypeError(HelperUtils().int_check_err(col))

            if df[col].max() > 1:
                raise TypeError(HelperUtils().int_max_check_err(col))

        # check analog ouputs [data with units of %] are floats only
        for col in [
            self.hot_water_bypass_vlv_cmd_col
        ]:
            if not pdtypes.is_float_dtype(df[col]):
                raise TypeError(HelperUtils().float_check_err(col))

            if df[col].max() > 1.0:
                raise TypeError(HelperUtils().float_max_check_err(col))

        df['flowmeter_check'] = (
            df[self.flow_meter_col] < self.hot_water_min_flow_stp - self.flow_meter_err_thres)

        df['bypass_vlv_check'] = (
            df[self.hot_water_bypass_vlv_cmd_col] >= .99 - self.hot_water_bypass_vlv_err_thres)

        df['pump_check'] = df[self.pump_status_bool_col] == 1

        df["fc5_flag"] = (df['flowmeter_check'] &
                          df['bypass_vlv_check'] &
                          df['pump_check']).astype(int)

        if self.troubleshoot:
            print("Troubleshoot mode enabled - not removing helper columns")

        else:
            del df['flowmeter_check']
            del df['bypass_vlv_check']
            del df['pump_check']

        return df


class FaultConditionSix:
    """OS2,3 - Hot water system not meeting supply setpoint"""

    def __init__(
        self,
        hot_water_temp_err_thres: float,
        hot_water_supply_temp_col: str,
        hot_water_supply_temp_spt_col: str,
        pump_status_bool_col: str,
        troubleshoot=False
    ):
        self.hot_water_temp_err_thres = hot_water_temp_err_thres
        self.hot_water_supply_temp_col = hot_water_supply_temp_col
        self.hot_water_supply_temp_spt_col = hot_water_supply_temp_spt_col
        self.pump_status_bool_col = pump_status_bool_col
        self.troubleshoot = troubleshoot

    def apply(self, df: pd.DataFrame) -> pd.DataFrame:

        # check if motor status is an int only
        for col in [
            self.pump_status_bool_col
        ]:
            if not pdtypes.is_integer_dtype(df[col]):
                raise TypeError(HelperUtils().int_check_err(col))

            if df[col].max() > 1:
                raise TypeError(HelperUtils().int_max_check_err(col))

        df['hw_spt_check'] = df[self.hot_water_supply_temp_col] + \
            self.hot_water_temp_err_thres < self.hot_water_supply_temp_spt_col

        df['pump_check'] = df[self.pump_status_bool_col] == 1

        df["fc6_flag"] = (df['hw_spt_check'] &
                          df['pump_check']).astype(int)

        if self.troubleshoot:
            print("Troubleshoot mode enabled - not removing helper columns")

        else:
            del df['hw_spt_check']
            del df['pump_check']

        return df


class FaultConditionSeven:
    """OS1,2,3 - Hot water system static/gauge pressure low"""

    def __init__(
        self,
        expansion_tank_press_stp: float,
        hot_water_sys_gauge_pres_col: str,
        pump_status_bool_col: str,
        troubleshoot=False
    ):
        self.expansion_tank_press_stp = expansion_tank_press_stp
        self.hot_water_sys_gauge_pres_col = hot_water_sys_gauge_pres_col
        self.pump_status_bool_col = pump_status_bool_col
        self.troubleshoot = troubleshoot

    def apply(self, df: pd.DataFrame) -> pd.DataFrame:

        # check if motor status is an int only
        for col in [
            self.pump_status_bool_col
        ]:
            if not pdtypes.is_integer_dtype(df[col]):
                raise TypeError(HelperUtils().int_check_err(col))

            if df[col].max() > 1:
                raise TypeError(HelperUtils().int_max_check_err(col))

        df['hw_sys_static_press_check'] = df[self.hot_water_sys_gauge_pres_col] < self.expansion_tank_press_stp * .9

        df['pump_check'] = df[self.pump_status_bool_col] == 1

        df["fc7_flag"] = (df['hw_sys_static_press_check'] &
                          df['pump_check']).astype(int)

        if self.troubleshoot:
            print("Troubleshoot mode enabled - not removing helper columns")

        else:
            del df['hw_sys_static_press_check']
            del df['pump_check']

        return df


class FaultConditionEight:
    """OS2,3 - Hot return temp too high for a condensing boiler to achieve high efficiency"""

    def __init__(
        self,
        hot_water_temp_err_thres: float,
        boiler_condensing_temp: float,
        hot_water_return_temp_col: str,
        pump_status_bool_col: str,
        troubleshoot=False
    ):
        self.hot_water_temp_err_thres = hot_water_temp_err_thres
        self.boiler_condensing_temp = boiler_condensing_temp
        self.hot_water_return_temp_col = hot_water_return_temp_col
        self.pump_status_bool_col = pump_status_bool_col
        self.troubleshoot = troubleshoot

    def apply(self, df: pd.DataFrame) -> pd.DataFrame:

        # check if motor status is an int only
        for col in [
            self.pump_status_bool_col
        ]:
            if not pdtypes.is_integer_dtype(df[col]):
                raise TypeError(HelperUtils().int_check_err(col))

            if df[col].max() > 1:
                raise TypeError(HelperUtils().int_max_check_err(col))

        df['boiler_condensing_check'] = df[self.hot_water_return_temp_col] - \
            self.hot_water_temp_err_thres > self.boiler_condensing_temp

        df['pump_check'] = df[self.pump_status_bool_col] == 1

        df["fc8_flag"] = (df['boiler_condensing_check'] &
                          df['pump_check']).astype(int)

        if self.troubleshoot:
            print("Troubleshoot mode enabled - not removing helper columns")

        else:
            del df['boiler_condensing_check']
            del df['pump_check']

        return df


class FaultConditionNine:
    """OS2,3 - Hot return temp too low for a NON condensing boiler, it will damage heat exchanger"""

    def __init__(
        self,
        hot_water_temp_err_thres: float,
        boiler_condensing_temp: float,
        hot_water_return_temp_col: str,
        pump_status_bool_col: str,
        troubleshoot=False
    ):
        self.hot_water_temp_err_thres = hot_water_temp_err_thres
        self.boiler_condensing_temp = boiler_condensing_temp
        self.hot_water_return_temp_col = hot_water_return_temp_col
        self.pump_status_bool_col = pump_status_bool_col
        self.troubleshoot = troubleshoot

    def apply(self, df: pd.DataFrame) -> pd.DataFrame:

        # check if motor status is an int only
        for col in [
            self.pump_status_bool_col
        ]:
            if not pdtypes.is_integer_dtype(df[col]):
                raise TypeError(HelperUtils().int_check_err(col))

            if df[col].max() > 1:
                raise TypeError(HelperUtils().int_max_check_err(col))

        df['boiler_condensing_check'] = df[self.hot_water_return_temp_col] + \
            self.hot_water_temp_err_thres < self.boiler_condensing_temp

        df['pump_check'] = df[self.pump_status_bool_col] == 1

        df["fc9_flag"] = (df['boiler_condensing_check'] &
                          df['pump_check']).astype(int)

        if self.troubleshoot:
            print("Troubleshoot mode enabled - not removing helper columns")

        else:
            del df['boiler_condensing_check']
            del df['pump_check']

        return df

    class FaultConditionTen:

        '''
        OS2 - Boiler leaving temp and hot water sys
        common hw water plant header temp mismatch
        '''

    def __init__(
        self,
        hot_water_temp_err_thres: float,
        flow_meter_col: str,
        boiler_leaving_temp_col: float,
        hot_water_supply_temp_col: str,
        boiler_status_bool_col: str,
        troubleshoot=False
    ):
        self.hot_water_temp_err_thres = hot_water_temp_err_thres
        self.flow_meter_col = flow_meter_col
        self.boiler_leaving_temp_col = boiler_leaving_temp_col
        self.hot_water_supply_temp_col = hot_water_supply_temp_col
        self.boiler_status_bool_col = boiler_status_bool_col
        self.troubleshoot = troubleshoot

    def apply(self, df: pd.DataFrame) -> pd.DataFrame:

        # check if motor status is an int only
        for col in [
            self.boiler_status_bool_col
        ]:
            if not pdtypes.is_integer_dtype(df[col]):
                raise TypeError(HelperUtils().int_check_err(col))

            if df[col].max() > 1:
                raise TypeError(HelperUtils().int_max_check_err(col))

        df['boiler_vs_header_check'] = abs((df[self.flow_meter_col] * df[self.boiler_leaving_temp_col]) /
                                           df[self.flow_meter_col] - df[self.hot_water_supply_temp_col]) > self.hot_water_temp_err_thres

        df['boiler_check'] = df[self.boiler_status_bool_col] == 1

        df["fc10_flag"] = (df['boiler_vs_header_check'] &
                           df['boiler_check']).astype(int)

        if self.troubleshoot:
            print("Troubleshoot mode enabled - not removing helper columns")

        else:
            del df['boiler_vs_header_check']
            del df['boiler_check']

        return df

    class FaultConditionEleven:

        '''
        OS2 - Boiler enter temp and hot water sys
        common hw water plant header temp mismatch
        '''

    def __init__(
        self,
        hot_water_temp_err_thres: float,
        flow_meter_col: str,
        boiler_enter_temp_col: float,
        hot_water_return_temp_col: str,
        boiler_status_bool_col: str,
        troubleshoot=False
    ):
        self.hot_water_temp_err_thres = hot_water_temp_err_thres
        self.flow_meter_col = flow_meter_col
        self.boiler_enter_temp_col = boiler_enter_temp_col
        self.hot_water_return_temp_col = hot_water_return_temp_col
        self.boiler_status_bool_col = boiler_status_bool_col
        self.troubleshoot = troubleshoot

    def apply(self, df: pd.DataFrame) -> pd.DataFrame:

        # check if motor status is an int only
        for col in [
            self.boiler_status_bool_col
        ]:
            if not pdtypes.is_integer_dtype(df[col]):
                raise TypeError(HelperUtils().int_check_err(col))

            if df[col].max() > 1:
                raise TypeError(HelperUtils().int_max_check_err(col))

        df['boiler_vs_header_check'] = abs((df[self.flow_meter_col] * df[self.boiler_enter_temp_col]) /
                                           df[self.flow_meter_col] - df[self.hot_water_return_temp_col]) > self.hot_water_temp_err_thres

        df['boiler_check'] = df[self.boiler_status_bool_col] == 1

        df["fc11_flag"] = (df['boiler_vs_header_check'] &
                           df['boiler_check']).astype(int)

        if self.troubleshoot:
            print("Troubleshoot mode enabled - not removing helper columns")

        else:
            del df['boiler_vs_header_check']
            del df['boiler_check']

        return df


class FaultConditionTwelve:
    """OS1,2,3: Excessive Entire Plant Cycling.
    Based on building loop or secondary pumps turning off and on
    """

    def __init__(
        self,
        plant_os_max: int,
        pump_vfd_speed_col: str,
        troubleshoot=False
    ):
        self.plant_os_max = plant_os_max
        self.pump_vfd_speed_col = pump_vfd_speed_col
        self.troubleshoot = troubleshoot

    # adds in these boolean columns to the dataframe
    def apply(self, df: pd.DataFrame) -> pd.DataFrame:

        # check analog ouputs [data with units of %] are floats only
        for col in [
            self.pump_vfd_speed_col
        ]:
            if not pdtypes.is_float_dtype(df[col]):
                raise TypeError(HelperUtils().float_check_err(col))

            if df[col].max() > 1.0:
                raise TypeError(HelperUtils().float_max_check_err(col))

        df['loop_pumps_on_mode'] = df[self.pump_vfd_speed_col] > .01
        df['loop_pumps_off_mode'] = df[self.pump_vfd_speed_col] == 0.0

        df = df.astype(int)

        # resample df and count pump starts and stops
        df = df.resample('H').apply(
            lambda x: (x.eq(1) & x.shift().ne(1)).sum())

        df["fc12_flag"] = df[df.columns].gt(
            self.plant_os_max).any(1).astype(int)

        if self.troubleshoot:
            print("Troubleshoot mode enabled - not removing helper columns")

        else:
            del df['loop_pumps_on_mode']
            del df['loop_pumps_off_mode']

        return df


class FaultConditionThirteen:
    """OS2,3: Excessive individual boiler cycling ON and OFF.
    Try and capture boiler itself or boiler circ pump.
    Assumption is the building loop or secondary is running.
    """

    def __init__(
        self,
        boiler_os_max: int,
        boiler_status_bool_col: str,
        troubleshoot=False
    ):
        self.boiler_os_max = boiler_os_max
        self.boiler_status_bool_col = boiler_status_bool_col
        self.troubleshoot = troubleshoot

    # adds in these boolean columns to the dataframe
    def apply(self, df: pd.DataFrame) -> pd.DataFrame:

        # check if motor status is an int only
        for col in [
            self.boiler_status_bool_col
        ]:
            if not pdtypes.is_integer_dtype(df[col]):
                raise TypeError(HelperUtils().int_check_err(col))

            if df[col].max() > 1:
                raise TypeError(HelperUtils().int_max_check_err(col))

        df['boiler_on_mode'] = df[self.boiler_status_bool_col] == 1
        df['boiler_off_mode'] = df[self.boiler_status_bool_col] == 0

        df = df.astype(int)

        # resample df and count boiler start and stops
        df = df.resample('H').apply(
            lambda x: (x.eq(1) & x.shift().ne(1)).sum())

        df["fc13_flag"] = df[df.columns].gt(
            self.boiler_os_max).any(1).astype(int)

        if self.troubleshoot:
            print("Troubleshoot mode enabled - not removing helper columns")

        else:
            del df['boiler_on_mode']
            del df['boiler_off_mode']

        return df


class FaultConditionFourteen:
    """OS 1,2,3: Excessive boiler staging. Stage number most likely
    a boiler integration represented as an int like stage 1,2,3,4
    """

    def __init__(
        self,
        boiler_stage_os_max: int,
        boiler_stage_int_col: str,
        troubleshoot=False
    ):
        self.boiler_stage_os_max = boiler_stage_os_max
        self.boiler_stage_int_col = boiler_stage_int_col
        self.troubleshoot = troubleshoot

    # adds in these boolean columns to the dataframe
    def apply(self, df: pd.DataFrame) -> pd.DataFrame:

        # check if motor status is an int only
        for col in [
            self.boiler_stage_int_col
        ]:
            if not pdtypes.is_integer_dtype(df[col]):
                raise TypeError(HelperUtils().int_check_err(col))

        # calc stage change with .diff()
        df['boiler_stage_change'] = abs(
            df[self.boiler_stage_int_col].diff()).dropna()

        df = df.astype(int)

        # resample df and count boiler start and stops
        df = df.resample('H').apply(
            lambda x: (x.eq(1) & x.shift().ne(1)).sum())

        df["fc14_flag"] = df[df.columns].gt(
            self.boiler_stage_os_max).any(1).astype(int)

        if self.troubleshoot:
            print("Troubleshoot mode enabled - not removing helper columns")

        else:
            del df['boiler_stage_change']

        return df
