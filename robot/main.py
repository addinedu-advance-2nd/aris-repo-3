

import sys
import time
import traceback
from xarm import version
from xarm.wrapper import XArmAPI

class RobotMain(object):
    """Robot Main Class"""
    def __init__(self, robot, **kwargs):
        self.alive = True
        self._arm = robot
        self._tcp_speed = 100
        self._tcp_acc = 2000
        self._angle_speed = 70
        self._angle_acc = 500
        self.state = 'icecreaming'

        self.position_home = [179.2, -42.1, 7.4, 186.7, 41.5, 0]  # angle
        self.position_jig_A_grab = [-257.3, -138.3, 192.1, 68.3, 86.1, -47.0] #linear
        self.position_jig_B_grab = [-153.3, -129.0, 192.8, 4.8, 89.0, -90.7] #linear
        self.position_jig_C_grab = [-79.8, -145.6, 194.4, 4.0, 88.9, -51.8] #linear
        self.position_jig_A_serve = [-258.7, -136.4, 211.2, 43.4, 88.7, -72.2] #Linear
        self.position_jig_B_serve = [-166.8, -126.5, 202.9, -45.2, 89.2, -133.6] #Linear
        self.position_jig_C_serve = [-63.1, -138.2, 203, -45.5, 88.1, -112.1] #Linear
        self.position_capsule_grab = [241.5, 136.0, 463.5, -140.1, 88.0, -52.5] #Linear

    # Robot init
    def _robot_init(self):
        self._arm.clean_warn()
        self._arm.clean_error()
        self._arm.motion_enable(True)
        self._arm.set_mode(0)
        self._arm.set_state(0)
        time.sleep(1)

    def _check_code(self, code, label):
        if code != 0:
            self.alive = False
            ret1 = self._arm.get_state()
            ret2 = self._arm.get_err_warn_code()
            self.pprint('{}, code={}, connected={}, state={}, error={}, ret1={}, ret2={}'.format(
                label, code, self._arm.connected, self._arm.state, self._arm.error_code, ret1, ret2))
        return self.alive

    @staticmethod
    def pprint(*args, **kwargs):
        try:
            stack_tuple = traceback.extract_stack(limit=2)[0]
            print('[{}][{}] {}'.format(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), stack_tuple[1], ' '.join(map(str, args))))
        except:
            print(*args, **kwargs)
# --------------------------------------------------------------왼쪽 홈 포지션------------------------------------------------
    def home_L(self):
        # Joint Motion
        print("Starting home_L")
        code = self._arm.set_cgpio_analog(0, 0)
        if not self._check_code(code, 'set_cgpio_analog'):
            return
        code = self._arm.set_cgpio_analog(1, 0)
        if not self._check_code(code, 'set_cgpio_analog'):
            return
        
        code = self._arm.set_cgpio_digital(0, 0, delay_sec=0)
        if not self._check_code(code, 'set_cgpio_digital'):
            return

        code = self._arm.set_servo_angle(angle=self.position_home, speed=self._angle_speed,
                                          mvacc=self._angle_acc, wait=True, radius=0.0)
        if not self._check_code(code, 'set_servo_angle'):
            return

        print('home_L finish')
        
#-----------------------------------------------------------오른쪽 홈포지션-------------------------------------------
    def home_R(self):
        # Joint Motion
        print("Starting home_R")
        code = self._arm.set_cgpio_analog(0, 0)
        if not self._check_code(code, 'set_cgpio_analog'):
            return
        code = self._arm.set_cgpio_analog(1, 0)
        if not self._check_code(code, 'set_cgpio_analog'):
            return
        
        code = self._arm.set_cgpio_digital(0, 0, delay_sec=0)
        if not self._check_code(code, 'set_cgpio_digital'):
            return

        code = self._arm.set_servo_angle(angle=[-6.1, 4.0, 29.8, 86.9, 93.5, 27.6], speed=self._angle_speed,
                                          mvacc=self._angle_acc, wait=True, radius=0.0)
        if not self._check_code(code, 'set_servo_angle'):
            return
        print('home_R finish')

#-------------------------------------------왼쪽에서 오른쪽 홈포지션으로 이동------------------------------------------
    def home_L_to_R(self):
            code = self._arm.set_position(*[-156.7, 7.0, 310.9, 81.1, 90.0, -104.1], speed=self._tcp_speed, mvacc=self._tcp_acc, radius=0.0, wait=False)
            if not self._check_code(code, 'set_position'):
                return
            code = self._arm.set_servo_angle(angle=[146.1, -10.7, 10.9, 102.7, 92.4, 24.9], speed=self._angle_speed, mvacc=self._angle_acc, wait=False, radius=20.0)
            if not self._check_code(code, 'set_servo_angle'):
                return
            code = self._arm.set_servo_angle(angle=[81.0, -10.8, 6.9, 103.6, 88.6, 9.6], speed=self._angle_speed, mvacc=self._angle_acc, wait=False, radius=40.0)
            if not self._check_code(code, 'set_servo_angle'):
                return
            code = self._arm.set_servo_angle(angle=[10.0, -20.8, 7.1, 106.7, 79.9, 26.0], speed=self._angle_speed, mvacc=self._angle_acc, wait=False, radius=50.0)
            if not self._check_code(code, 'set_servo_angle'):
                return
            code = self._arm.set_servo_angle(angle=[-6.1, 4.0, 29.8, 86.9, 93.5, 27.6], speed=self._angle_speed, mvacc=self._angle_acc, wait=False, radius=0.0)
            if not self._check_code(code, 'set_servo_angle'):
                return

#--------------------------------------------------------오른쪽에서 왼쪽 홈포지션으로 이동-----------------------------------------
    def home_R_to_L(self):
        code = self._arm.set_servo_angle(angle=[-6.1, 4.0, 29.8, 86.9, 93.5, 27.6], speed=self._angle_speed, mvacc=self._angle_acc, wait=False, radius=0.0)
        if not self._check_code(code, 'set_servo_angle'):
            return
        code = self._arm.set_servo_angle(angle=[-6.1, -19.5, 8.1, 87.4, 93.8, 24.4], speed=self._angle_speed, mvacc=self._angle_acc, wait=False, radius=0.0)
        if not self._check_code(code, 'set_servo_angle'):
            return
        code = self._arm.set_servo_angle(angle=[124.7, -19.5, 8.1, 87.4, 93.8, 24.4], speed=self._angle_speed, mvacc=self._angle_acc, wait=False, radius=0.0)
        if not self._check_code(code, 'set_servo_angle'):
            return
        code = self._arm.set_position(*[-156.7, 7.0, 310.9, 81.1, 90.0, -104.1], speed=self._tcp_speed, mvacc=self._tcp_acc, radius=0.0, wait=False)
        if not self._check_code(code, 'set_position'):
            return

    def home_R_to_serving(self):
        code = self._arm.set_servo_angle(angle=[-6.1, 4.0, 29.8, 86.9, 93.5, 27.6], speed=self._angle_speed, mvacc=self._angle_acc, wait=False, radius=0.0)
        if not self._check_code(code, 'set_servo_angle'):
            return
        code = self._arm.set_servo_angle(angle=[-6.1, -19.5, 8.1, 87.4, 93.8, 24.4], speed=self._angle_speed, mvacc=self._angle_acc, wait=False, radius=0.0)
        if not self._check_code(code, 'set_servo_angle'):
            return
        code = self._arm.set_servo_angle(angle=[124.7, -19.5, 8.1, 87.4, 93.8, 24.4], speed=self._angle_speed, mvacc=self._angle_acc, wait=False, radius=0.0)
        if not self._check_code(code, 'set_servo_angle'):
            return
        code = self._arm.set_position(*[-162.3, -20.2, 237.4, -9.1, 86.9, -101.8], speed=self._tcp_speed, mvacc=self._tcp_acc, radius=0.0, wait=False)
        if not self._check_code(code, 'set_position'):
            return

# -----------------------------------------------A,B,C 구역 아이스크림 캡술 잡는 동작 구현----------------------------------------------------------
    def motion_grab_capsule(self, jig_num):
        # Joint Motion
        print("Starting grab_capsule")
        code = self._arm.set_cgpio_analog(0, 5)
        if not self._check_code(code, 'set_cgpio_analog'):
            return
        code = self._arm.set_cgpio_analog(1, 5)
        if not self._check_code(code, 'set_cgpio_analog'):
            return
        
        self._angle_speed = 100
        self._angle_acc = 100

        self._tcp_speed = 100
        self._tcp_acc = 1000

        #code = self._arm.stop_lite6_gripper()
        #if not self._check_code(code, 'stop_lite6_gripper'):
        #    return
        #time.sleep(0.5)

        code = self._arm.set_servo_angle(angle=[166.1, 30.2, 25.3, 75.3, 93.9, -5.4], speed=self._angle_speed,
                                            mvacc=self._angle_acc, wait=True, radius=0.0)
        if not self._check_code(code, 'set_servo_angle'):
            return   
               
        code = self._arm.open_lite6_gripper()
        if not self._check_code(code, 'open_lite6_gripper'):
            return
        time.sleep(1)

        if jig_num == 'A':
            code = self._arm.set_servo_angle(angle=[193.6, 39.1, 50.7, 119.8, 83.4, 9.1], speed=self._angle_speed,
                                             mvacc=self._angle_acc, wait=True, radius=0.0)
            if not self._check_code(code, 'set_servo_angle'):
                return
            
        elif jig_num == 'B':
            code = self._arm.set_position(*self.position_jig_B_grab, speed=self._tcp_speed,
                                          mvacc=self._tcp_acc, radius=0.0, wait=True)
            if not self._check_code(code, 'set_position'):
                return
            
        elif jig_num == 'C':
            code = self._arm.set_servo_angle(angle=[182.6, 27.8, 27.7, 55.7, 90.4, -6.4], speed=self._angle_speed,
                                             mvacc=self._angle_acc, wait=True, radius=0.0)
            if not self._check_code(code, 'set_servo_angle'):
                return
            
            code = self._arm.set_position(*self.position_jig_C_grab, speed=self._tcp_speed,
                                          mvacc=self._tcp_acc, radius=0.0, wait=True)
            if not self._check_code(code, 'set_position'):
                return

        code = self._arm.close_lite6_gripper()
        if not self._check_code(code, 'close_lite6_gripper'):
            return
        time.sleep(2)
        
        if jig_num == 'C':
            code = self._arm.set_position(z=150, radius=0, speed=self._tcp_speed, mvacc=self._tcp_acc, relative=True,
                                          wait=False)
            if not self._check_code(code, 'set_position'):
                return

            code = self._arm.set_tool_position(*[0.0, 0.0, -90.0, 0.0, 0.0, 0.0], speed=self._tcp_speed,
                                               mvacc=self._tcp_acc, wait=True)
            if not self._check_code(code, 'set_position'):
                return
        else:
            code = self._arm.set_position(z=100, radius=0, speed=self._tcp_speed, mvacc=self._tcp_acc, relative=True,
                                          wait=False)
            if not self._check_code(code, 'set_position'):
                return

        self._angle_speed = 140
        self._angle_acc = 170
        # ------------- 컵 잡고난 후 최종위치 ------
        code = self._arm.set_servo_angle(angle=[146.1, -10.7, 10.9, 102.7, 92.4, 24.9], speed=self._angle_speed,
                                         mvacc=self._angle_acc, wait=False, radius=20.0)
        if not self._check_code(code, 'set_servo_angle'):
            return
        
        self._tcp_speed = 100
        self._tcp_acc = 2000
        self._angle_speed = 70
        self._angle_acc = 500
        print('motion_grab_capsule finish')

# -----------------------------------------캡슐을 프레스까지 이동후 위치-------------------------------------------------------
    def motion_place_capsule(self):
        print("Starting place_capsule")
        code = self._arm.set_servo_angle(angle=[81.0, -10.8, 6.9, 103.6, 88.6, 9.6], speed=self._angle_speed, mvacc=self._angle_acc, wait=False, radius=40.0)
        if not self._check_code(code, 'set_servo_angle'):
            return
        code = self._arm.set_servo_angle(angle=[10.0, -20.8, 7.1, 106.7, 79.9, 26.0], speed=self._angle_speed, mvacc=self._angle_acc, wait=False, radius=50.0)
        if not self._check_code(code, 'set_servo_angle'):
            return
        code = self._arm.set_servo_angle(angle=[8.4, -42.7, 23.7, 177.4, 31.6, 3.6], speed=self._angle_speed, mvacc=self._angle_acc, wait=False, radius=40.0)
        if not self._check_code(code, 'set_servo_angle'):
            return
        code = self._arm.set_servo_angle(angle=[8.4, -32.1, 55.1, 96.6, 29.5, 81.9], speed=self._angle_speed, mvacc=self._angle_acc, wait=False, radius=0.0)
        if not self._check_code(code, 'set_servo_angle'):
            return
        code = self._arm.set_position(*[237.0, 135.8, 486.4, -143.8, 89.4, -57.3], speed=self._tcp_speed, mvacc=self._tcp_acc, radius=0.0, wait=False)
        if not self._check_code(code, 'set_position'):
            return
        code = self._arm.set_position(*[237.0, 135.8, 461.4, -143.8, 89.4, -57.3], speed=self._tcp_speed, mvacc=self._tcp_acc, radius=0.0, wait=False)
        if not self._check_code(code, 'set_position'):
            return
        code = self._arm.set_cgpio_analog(0, 5)
        if not self._check_code(code, 'set_cgpio_analog'):
            return
        code = self._arm.set_cgpio_analog(1, 5)
        if not self._check_code(code, 'set_cgpio_analog'):
            return
    


        time.sleep(3)
        code = self._arm.open_lite6_gripper()
        if not self._check_code(code, 'open_lite6_gripper'):
            return
        time.sleep(3)


        '''code = self._arm.set_servo_angle(angle=[-4, -0.6, 73.3, 88.5, 93.5, 75.1], speed=self._angle_speed, mvacc=self._angle_acc, wait=False, radius=0.0)
        if not self._check_code(code, 'set_servo_angle'):
            return
        code = self._arm.set_servo_angle(angle=[-24.9, -2.1, 60.4, 82.6, 106.2, 35.3], speed=self._angle_speed, mvacc=self._angle_acc, wait=False, radius=0.0)
        if not self._check_code(code, 'set_servo_angle'):
            return
        self.home_R()'''


        print('motion_place_capsule finish')
# --------------------------------- 빈 컵 잡으러 가기 -------------------------------------------------------
    def motion_grab_cup(self):
            print("starting grab cup")

            self._tcp_speed = 100
            self._tcp_acc = 2000
            self._angle_speed = 80
            self._angle_acc = 500

            code = self._arm.set_cgpio_analog(0, 0)
            if not self._check_code(code, 'set_cgpio_analog'):
                return

            code = self._arm.set_cgpio_analog(1, 5)
            if not self._check_code(code, 'set_cgpio_analog'):
                return
            time.sleep(2)


            #code = self._arm.set_servo_angle(angle=[-6.1, 4.0, 29.8, 86.9, 93.5, 27.6], speed=self._angle_speed, mvacc=self._angle_acc, wait=False, radius=0.0)
            #if not self._check_code(code, 'set_servo_angle'):
            #    return
            code = self._arm.set_servo_angle(angle=[-4, -0.6, 73.3, 88.5, 93.5, 75.1], speed=self._angle_speed, mvacc=self._angle_acc, wait=False, radius=0.0)
            if not self._check_code(code, 'set_servo_angle'):
                return
            code = self._arm.set_servo_angle(angle=[-24.9, -2.1, 60.4, 82.6, 106.2, 58.7], speed=self._angle_speed, mvacc=self._angle_acc, wait=False, radius=0.0)
            if not self._check_code(code, 'set_servo_angle'):
                return
            code = self._arm.set_servo_angle(angle=[-6.1, -5.2, 53.5, -94.7, 87.6, 113.7], speed=self._angle_speed, mvacc=self._angle_acc, wait=False, radius=0.0)
            if not self._check_code(code, 'set_servo_angle'):
                return
            code = self._arm.set_servo_angle(angle=[9.9, 43.8, 34.9, -80.3, 84.3, 187.9], speed=self._angle_speed, mvacc=self._angle_acc, wait=False, radius=0.0)
            if not self._check_code(code, 'set_servo_angle'):
                return
            code = self._arm.set_position(*[179.1, -93.4, 146.2, -94.3, -87.5, -171.9], speed=self._tcp_speed, mvacc=self._tcp_acc, radius=0.0, wait=False)
            if not self._check_code(code, 'set_position'):
                return
            time.sleep(1.5)
            code = self._arm.close_lite6_gripper()
            if not self._check_code(code, 'close_lite6_gripper'):
                return
            time.sleep(4.5)
            code = self._arm.set_position(*[179.1, -93.4, 336.0, -94.3, -87.5, -171.9], speed=self._tcp_speed, mvacc=self._tcp_acc, radius=0.0, wait=False)
            if not self._check_code(code, 'set_position'):
                return
            code = self._arm.set_servo_angle(angle=[-11.0, -13.8, 39.9, -27.2, 55.8, 93.4], speed=self._angle_speed, mvacc=self._angle_acc, wait=False, radius=0.0)
            if not self._check_code(code, 'set_servo_angle'):
                return
            code = self._arm.set_position(*[2.7, 135.4, 367.1, 154.9, 89.4, -111.4], speed=self._tcp_speed, mvacc=self._tcp_acc, radius=0.0, wait=False)
            if not self._check_code(code, 'set_position'):
                return
            time.sleep(1)
            code = self._arm.open_lite6_gripper()
            if not self._check_code(code, 'open_lite6_gripper'):
                return
  

            print('motion_place_capsule finish')

# ------------------------------------- 토핑 얻으러 가기 --------------------------------------------------------------------
    def motion_topping(self, topping_num):
        #self.home_R()
        #self.home_R_to_L()
        #time.sleep(1)
        #self.home_L()
        code = self._arm.set_position(*[2.8, 143.1, 373.1, 148.6, 89.4, -117.8], speed=self._tcp_speed, mvacc=self._tcp_acc, radius=0.0, wait=False)
        if not self._check_code(code, 'set_position'):
            return

        # 1번째 토핑 부분
        if topping_num==0:
            code = self._arm.set_position(*[-258.7, 143.4, 373.1, 148.6, 89.4, -117.8], speed=self._tcp_speed, mvacc=self._tcp_acc, radius=0.0, wait=False)
            if not self._check_code(code, 'set_position'):
                return
        elif topping_num==1:
            code = self._arm.set_position(*[-136.6, 143.4, 373.1, 148.6, 89.4, -117.8], speed=self._tcp_speed, mvacc=self._tcp_acc, radius=0.0, wait=False)
            if not self._check_code(code, 'set_position'):
                return
        else:
            code = self._arm.set_position(*[2.8, 143.1, 373.1, 148.6, 89.4, -117.8], speed=self._tcp_speed, mvacc=self._tcp_acc, radius=0.0, wait=False)
            if not self._check_code(code, 'set_position'):
                return
        time.sleep(8)

# --------------------------------------------- 아이스크림 뽑기 ----------------------------------------------------
    def motion_make_icecream(self):
    
        code = self._arm.set_cgpio_digital(3, 1, delay_sec=0)
        if not self._check_code(code, 'set_cgpio_digital'):
            return
        code = self._arm.set_position(*[256.6, 143.4, 373.1, 148.6, 89.4, -117.8], speed=self._tcp_speed, mvacc=self._tcp_acc, radius=0.0, wait=False)
        if not self._check_code(code, 'set_position'):
            return
        time.sleep(11)

        code = self._arm.set_cgpio_digital(3, 0, delay_sec=0)
        if not self._check_code(code, 'set_cgpio_digital'):
            return

        self.home_R()
       
# --------------------------------------------- 서빙 ----------------------------------------------------
    def serving(self, position):
        self.icecream_place_position = position
        self.home_R_to_serving()
        code = self._arm.set_position(*[-162.3, -20.2, 237.4, -9.1, 86.9, -101.8], speed=self._tcp_speed, mvacc=self._tcp_acc, radius=0.0, wait=False)
        if not self._check_code(code, 'set_position'):
            return
        if self.icecream_place_position == 'A':
            code = self._arm.set_position(*[-302.0, -20.2, 237.4, -9.1, 86.9, -101.8], speed=self._tcp_speed, mvacc=self._tcp_acc, radius=0.0, wait=False)
            if not self._check_code(code, 'set_position'):
                return
            code = self._arm.set_position(*[-302.0, -125.4, 237.4, -9.1, 86.9, -101.8], speed=self._tcp_speed, mvacc=self._tcp_acc, radius=0.0, wait=False)
            if not self._check_code(code, 'set_position'):
                return
            code = self._arm.set_position(*[-302.0, -125.4, 188.8, -9.1, 86.9, -101.8], speed=self._tcp_speed, mvacc=self._tcp_acc, radius=0.0, wait=False)
            if not self._check_code(code, 'set_position'):
                return
            code = self._arm.set_position(*[-302.0, -38.1, 188.8, -9.1, 86.9, -101.8], speed=self._tcp_speed, mvacc=self._tcp_acc, radius=0.0, wait=False)
            if not self._check_code(code, 'set_position'):
                return
        if self.icecream_place_position == 'B':
            code = self._arm.set_position(*[-162.3, -124.8, 237.4, -9.1, 86.9, -101.8], speed=self._tcp_speed, mvacc=self._tcp_acc, radius=0.0, wait=False)
            if not self._check_code(code, 'set_position'):
                return
            code = self._arm.set_position(*[-162.3, -124.8, 188.8, -9.1, 86.9, -101.8], speed=self._tcp_speed, mvacc=self._tcp_acc, radius=0.0, wait=False)
            if not self._check_code(code, 'set_position'):
                return
            code = self._arm.set_position(*[-162.3, -28.2, 188.8, -9.1, 86.9, -101.8], speed=self._tcp_speed, mvacc=self._tcp_acc, radius=0.0, wait=False)
            if not self._check_code(code, 'set_position'):
                return
        if self.icecream_place_position == 'C':
            code = self._arm.set_position(*[-162.3, -20.2, 237.4, -9.1, 86.9, -101.8], speed=self._tcp_speed, mvacc=self._tcp_acc, radius=0.0, wait=False)
            if not self._check_code(code, 'set_position'):
                return
            code = self._arm.set_position(*[-160.3, -57.3, 241.3, -85.9, 83.7, -139.0], speed=self._tcp_speed, mvacc=self._tcp_acc, radius=0.0, wait=False)
            if not self._check_code(code, 'set_position'):
                return
            code = self._arm.set_servo_angle(angle=[219.8, 4.4, 17.5, 92.9, 89.8, 6.8], speed=self._angle_speed, mvacc=self._angle_acc, wait=False, radius=0.0)
            if not self._check_code(code, 'set_servo_angle'):
                return
            code = self._arm.set_position(*[-79.6, -146.2, 192.4, -85.8, 83.7, -138.9], speed=self._tcp_speed, mvacc=self._tcp_acc, radius=0.0, wait=False)
            if not self._check_code(code, 'set_position'):
                return
            code = self._arm.set_position(*[-160.3, -57.3, 192.4, -85.9, 83.7, -139.0], speed=self._tcp_speed, mvacc=self._tcp_acc, radius=0.0, wait=False)
            if not self._check_code(code, 'set_position'):
                return
            '''code = self._arm.set_position(*[-156.7, 7.0, 310.9, 81.1, 90.0, -104.1], speed=self._tcp_speed, mvacc=self._tcp_acc, radius=0.0, wait=False)
            if not self._check_code(code, 'set_position'):
                return'''
            
        code = self._arm.set_servo_angle(angle=[146.1, -10.7, 10.9, 102.7, 92.4, 24.9], speed=self._angle_speed,
                                        mvacc=self._angle_acc, wait=False, radius=20.0)
        if not self._check_code(code, 'set_servo_angle'):
            return    

# --------------------------------------------- 쓰레기 버리기 ----------------------------------------------------
    def throw_away_trash(self):
        #self.home_L_to_R()
        code = self._arm.set_servo_angle(angle=[81.0, -10.8, 6.9, 103.6, 88.6, 9.6], speed=self._angle_speed, mvacc=self._angle_acc, wait=False, radius=40.0)
        if not self._check_code(code, 'set_servo_angle'):
            return
        code = self._arm.set_servo_angle(angle=[10.0, -20.8, 7.1, 106.7, 79.9, 26.0], speed=self._angle_speed, mvacc=self._angle_acc, wait=False, radius=50.0)
        if not self._check_code(code, 'set_servo_angle'):
            return
        code = self._arm.set_servo_angle(angle=[-6.1, 4, 29.8, 86.9, 93.5, 27.6], speed=self._angle_speed, mvacc=self._angle_acc, wait=False, radius=50.0)
        if not self._check_code(code, 'set_servo_angle'):
            return
        code = self._arm.set_servo_angle(angle=[-21.4, -2.0, 77.4, 88.9, 102.9, 74.5], speed=self._angle_speed, mvacc=self._angle_acc, wait=False, radius=0.0)
        if not self._check_code(code, 'set_servo_angle'):
            return
        code = self._arm.set_position(*[237.0, 135.8, 461.4, -143.8, 89.4, -57.3], speed=self._tcp_speed, mvacc=self._tcp_acc, radius=0.0, wait=False)
        if not self._check_code(code, 'set_position'):
            return
        time.sleep(4)
        code = self._arm.close_lite6_gripper()
        if not self._check_code(code, 'close_lite6_gripper'):
            return
        time.sleep(4)
        code = self._arm.set_servo_angle(angle=[-21.4, -2.0, 77.4, 88.9, 102.9, 74.5], speed=self._angle_speed, mvacc=self._angle_acc, wait=False, radius=0.0)
        if not self._check_code(code, 'set_servo_angle'):
            return
        code = self._arm.set_servo_angle(angle=[-6.1, 4.0, 29.8, 86.9, 93.5, 27.6], speed=self._angle_speed, mvacc=self._angle_acc, wait=False, radius=0.0)
        if not self._check_code(code, 'set_servo_angle'):
            return
        time.sleep(1)
        code = self._arm.open_lite6_gripper()
        if not self._check_code(code, 'open_lite6_gripper'):
            return
        time.sleep(1)
        code = self._arm.set_servo_angle(angle=[17.6, 4.0, 27.9, 106.5, 79.3, 15.5], speed=self._angle_speed, mvacc=self._angle_acc, wait=False, radius=0.0)
        if not self._check_code(code, 'set_servo_angle'):
            return
        code = self._arm.set_servo_angle(angle=[17.6, 4.0, 27.9, 106.5, 79.3, -155.5], speed=self._angle_speed, mvacc=self._angle_acc, wait=False, radius=0.0)
        if not self._check_code(code, 'set_servo_angle'):
            return
        self.home_R()




# --------------------------------------------- 주문 맞게 서빙 ----------------------------------------------------
    def order_msg(self, capsule_position, topping, icecream_serving_position):
        self.capsule_num = capsule_position
        self.topping_num = topping
        self.motion_grab_capsule(self.capsule_num)
        self.motion_place_capsule()
        self.motion_grab_cup()
        self.motion_topping(self.topping_num)
        self.motion_make_icecream()
        self.serving(icecream_serving_position)
        self.throw_away_trash()
        self.home_R_to_L()
        time.sleep(1)
        code = self._arm.stop_lite6_gripper()
        if not self._check_code(code, 'stop_lite6_gripper'):
            return
        time.sleep(1)

#------------------------------run!!!!!!!!!!!!!!!------------------------------------------------------------------------



    '''def check_home_position(self):
        current_angles = self._arm.get_servo_angle()
        # 소수점 없는 정수로 비교
        if current_angles == [int(angle) for angle in self.position_home]:
            print("Currently at home_L position.")
            return 'home_L'
        elif current_angles == [-6, 4, 29, 86, 93, 27]:  # home_R 각도 (정수로 변경)
            print("Currently at home_R position.")
            return 'home_R'
        else:
            print("Currently at an unknown position.")
            return 'unknown'''
        


    def run(self):
        try:
            while self.alive:
                if self.state == 'icecreaming':
                    '''current_position = self.check_home_position()
                    if current_position == 'home_R':
                        self.home_R_to_L()  # home_R에 있다면 home_R_to_L 실행
                    elif current_position == 'home_L':
                        self.home_L()  # home_L에 있다면 home_L 실행
                    else:
                        print("Position not recognized. Please check the robot's state.")
                        return  # 위치가 인식되지 않으면 종료'''
                    self.home_L()
                    self.order_msg('B',2,'B')
                    #self.home_R()
                    #self.motion_grab_cup()
                    #self.home_R_to_L()
                    #self.motion_grab_cup()
                    #self.home_L_to_R()
                    #self.motion_make_icecream()
                    #time.sleep(1)rnrks
                    #self.home_R_to_L()
                    
                    #self.serving('C')
                    #self.throw_away_trash()
                    #self.motion_grab_capsule('B') 
                    #self.motion_place_capsule()
                    #self.motion_grab_cup()
                    #time.sleep(1)
                 

   
                    print('all finish')
                    self.state = 'ready'

        except Exception as e:
            self.pprint('MainException: {}'.format(e))
        self.alive = False

if __name__ == '__main__':
    RobotMain.pprint('xArm-Python-SDK Version:{}'.format(version.__version__))
    arm = XArmAPI('192.168.1.190', baud_checkset=False)
    robot_main = RobotMain(arm)
    robot_main._robot_init()
    robot_main.run()