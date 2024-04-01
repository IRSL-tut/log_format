#
# jupyter console --kernel=choreonoid
#
####
#
# exec(open('log_format/plot_using_model.py').read())
# setupRobot()
# dumpLogFiles(prefix, directory=filedir, robot=robot_c)
# calcLinkMovements(robot_r, lst_tm, lst_real_pos, lst_real_rot, lst_real_q, time=44.37)
# calcLinkMovements(robot_c, lst_tm, lst_ctrl_pos, lst_ctrl_rot, lst_ctrl_q, time=44.37)
#targetTime=38.0
#prefix='chidori_mj00_0.33m_1.0sec_Bgain1.0'
exec(open('/choreonoid_ws/install/share/irsl_choreonoid/sample/irsl_import.py').read())

targetTime=44.6
prefix='chidori_mj00_0.33m_1.0sec'
filedir='logs/{}'.format(prefix)

#
n_ctrl_rot = '{}/{}.{}'.format(filedir, prefix, 'CentroidalManager_IRSL_LOG_ControlRobot_orientation')
n_ctrl_pos = '{}/{}.{}'.format(filedir, prefix, 'CentroidalManager_IRSL_LOG_ControlRobot_position')
n_ctrl_q   = '{}/{}.{}'.format(filedir, prefix, 'CentroidalManager_IRSL_LOG_ControlRobot_q')
#CentroidalManager_IRSL_LOG_PlannedRobot_dcm
#CentroidalManager_IRSL_LOG_RealRobot_dcm
n_real_rot = '{}/{}.{}'.format(filedir, prefix, 'CentroidalManager_IRSL_LOG_RealRobot_orientation')
n_real_pos = '{}/{}.{}'.format(filedir, prefix, 'CentroidalManager_IRSL_LOG_RealRobot_position')
n_real_q   = '{}/{}.{}'.format(filedir, prefix, 'CentroidalManager_IRSL_LOG_RealRobot_q')
#
lineNumber = int(targetTime*500)
#
f_ctrl_rot = open(n_ctrl_rot, mode='r')
f_ctrl_pos = open(n_ctrl_pos, mode='r')
f_ctrl_q   = open(n_ctrl_q  , mode='r')
#
f_real_rot = open(n_real_rot, mode='r')
f_real_pos = open(n_real_pos, mode='r')
f_real_q   = open(n_real_q  , mode='r')

lst_tm = []
lst_ctrl_rot = []
lst_ctrl_pos = []
lst_ctrl_q   = []
lst_real_rot = []
lst_real_pos = []
lst_real_q   = []

str_ctrl_rot=f_ctrl_rot.readline()
str_ctrl_pos=f_ctrl_pos.readline()
str_ctrl_q  =f_ctrl_q.readline()
str_real_rot=f_real_rot.readline()
str_real_pos=f_real_pos.readline()
str_real_q  =f_real_q.readline()

while str_ctrl_rot:
    lst_tm.append( float(str_ctrl_rot.split(' ')[0]) )
    lst_ctrl_rot.append( npa( [ float(v) for v in str_ctrl_rot.split(' ')[1:] ] ))
    lst_ctrl_pos.append( npa( [ float(v) for v in str_ctrl_pos.split(' ')[1:] ] ))
    lst_ctrl_q  .append( npa( [ float(v) for v in str_ctrl_q.split(' ')[1:] ]   ))
    lst_real_rot.append( npa( [ float(v) for v in str_real_rot.split(' ')[1:] ] ))
    lst_real_pos.append( npa( [ float(v) for v in str_real_pos.split(' ')[1:] ] ))
    lst_real_q  .append( npa( [ float(v) for v in str_real_q.split(' ')[1:] ]   ))

    str_ctrl_rot=f_ctrl_rot.readline()
    str_ctrl_pos=f_ctrl_pos.readline()
    str_ctrl_q  =f_ctrl_q.readline()
    str_real_rot=f_real_rot.readline()
    str_real_pos=f_real_pos.readline()
    str_real_q  =f_real_q.readline()

f_ctrl_rot.close()
f_ctrl_pos.close()
f_ctrl_q  .close()
#
f_real_rot.close()
f_real_pos.close()
f_real_q  .close()

###
def calcLinkMovements(robot, lst_tm, lst_pos, lst_rot, lst_q, time=None, index=1):
    if time is not None:
        idx_cur  = int(time*500)
    else:
        idx_cur  = index
    idx_prev = idx_cur - 1
    ##
    tm_cur  = lst_tm[idx_cur]
    tm_prev = lst_tm[idx_prev]
    tm_diff = tm_cur - tm_prev
    ##
    pos_cur  = lst_pos[idx_cur]
    pos_prev = lst_pos[idx_prev]
    rot_cur  = lst_rot[idx_cur]
    rot_prev = lst_rot[idx_prev]
    q_cur  = lst_q[idx_cur]
    q_prev = lst_q[idx_prev]
    #
    dq = (q_cur - q_prev)/tm_diff
    #
    cds_prev=coordinates(pos_prev)
    cds_prev.setRPY(rot_prev)
    cds_cur=coordinates(pos_cur)
    cds_cur.setRPY(rot_cur)
    cds_diff = cds_prev.transformation(cds_cur)
    #
    vel   = cds_diff.pos/tm_diff
    omega = cutil.omegaFromRot(cds_diff.rot)/tm_diff
    cds_cur.rotateVector(vel)
    cds_cur.rotateVector(omega)
    robot.robot.rootLink.v = vel
    robot.robot.rootLink.w = omega
    #
    robot.rootCoords(cds_cur)
    #
    robot.angleVector(q_cur)
    #
    for i, j in enumerate(robot.jointList):
        j.dq = dq[i]
    #
    robot.robot.calcForwardKinematics(True)
    robot.robot.calcCenterOfMass()

def setupRobot(modelFile='CHIDORI/model/CHIDORImain.wrl'):
    global r_ctrl, r_real, robot_c, robot_r
    # exec(open('/choreonoid_ws/install/share/irsl_choreonoid/sample/irsl_import.py').read())
    ## choreonoid check
    r_ctrl=ru.loadRobotItem(modelFile, name='Control')
    r_real=ru.loadRobotItem(modelFile, name='Real')
    robot_c=RobotModel(r_ctrl)
    ### here depends on the robot
    robot_c.registerEndEffector('rleg', ## end-effector
                                'RLEG_JOINT5', ## tip-link
                                tip_link_to_eef = ru.make_coordinates({'pos': [0, 0, -0.1065]}),
                                joint_tuples = (('RLEG_JOINT0', 'hip-y'),
                                                ('RLEG_JOINT1', 'hip-r'),
                                                ('RLEG_JOINT2', 'hip-p'),
                                                ('RLEG_JOINT3', 'knee-p'),
                                                ('RLEG_JOINT4', 'ankle-p'),
                                                ('RLEG_JOINT5', 'ankle-r'),
                                )
    )
    robot_c.registerEndEffector('lleg', ## end-effector
                                'LLEG_JOINT5', ## tip-link
                                tip_link_to_eef = ru.make_coordinates({'pos': [0, 0, -0.1065]}),
                                joint_tuples = (('LLEG_JOINT0', 'hip-y'),
                                                ('LLEG_JOINT1', 'hip-r'),
                                                ('LLEG_JOINT2', 'hip-p'),
                                                ('LLEG_JOINT3', 'knee-p'),
                                                ('LLEG_JOINT4', 'ankle-p'),
                                                ('LLEG_JOINT5', 'ankle-r'),
                                )
    )
    robot_r=RobotModel(r_real)
    ### here depends on the robot
    robot_r.registerEndEffector('rleg', ## end-effector
                                'RLEG_JOINT5', ## tip-link
                                tip_link_to_eef = ru.make_coordinates({'pos': [0, 0, -0.1065]}),
                                joint_tuples = (('RLEG_JOINT0', 'hip-y'),
                                                ('RLEG_JOINT1', 'hip-r'),
                                                ('RLEG_JOINT2', 'hip-p'),
                                                ('RLEG_JOINT3', 'knee-p'),
                                                ('RLEG_JOINT4', 'ankle-p'),
                                                ('RLEG_JOINT5', 'ankle-r'),
                                )
    )
    robot_r.registerEndEffector('lleg', ## end-effector
                                'LLEG_JOINT5', ## tip-link
                                tip_link_to_eef = ru.make_coordinates({'pos': [0, 0, -0.1065]}),
                                joint_tuples = (('LLEG_JOINT0', 'hip-y'),
                                                ('LLEG_JOINT1', 'hip-r'),
                                                ('LLEG_JOINT2', 'hip-p'),
                                                ('LLEG_JOINT3', 'knee-p'),
                                                ('LLEG_JOINT4', 'ankle-p'),
                                                ('LLEG_JOINT5', 'ankle-r'),
                                )
    )

def dumpLogFiles(prefix, robot, directory=None):
    if directory is None:
        directory = prefix

    fn_real_m = '{}/{}.Real_totalMomentum'.format(directory, prefix)
    fn_ctrl_m = '{}/{}.Control_totalMomentum'.format(directory, prefix)
    fn_real_lf = '{}/{}.Real_Left_FootPos'.format(directory, prefix)
    fn_real_rf = '{}/{}.Real_Right_FootPos'.format(directory, prefix)
    fn_ctrl_lf = '{}/{}.Control_Left_FootPos'.format(directory, prefix)
    fn_ctrl_rf = '{}/{}.Control_Right_FootPos'.format(directory, prefix)

    f_real_m  = open(fn_real_m,  mode='w')
    f_ctrl_m  = open(fn_ctrl_m,  mode='w')
    f_real_lf = open(fn_real_lf, mode='w')
    f_real_rf = open(fn_real_rf, mode='w')
    f_ctrl_lf = open(fn_ctrl_lf, mode='w')
    f_ctrl_rf = open(fn_ctrl_rf, mode='w')

    ## write Initial data
    print('0   0 0 0 0 0 0', file=f_real_m)
    print('0   0 0 0 0 0 0', file=f_real_lf)
    print('0   0 0 0 0 0 0', file=f_real_rf)
    print('0   0 0 0 0 0 0', file=f_ctrl_m)
    print('0   0 0 0 0 0 0', file=f_ctrl_lf)
    print('0   0 0 0 0 0 0', file=f_ctrl_rf)

    size=len(lst_tm)
    for i in range(size-1):
        idx = i+1
        ## real
        calcLinkMovements(robot, lst_tm, lst_real_pos, lst_real_rot, lst_real_q, index=idx)
        ##
        tm = lst_tm[idx]
        lf = robot.lleg.endEffector
        rf = robot.rleg.endEffector
        P, L = robot.robot.calcTotalMomentum()
        ##
        print('{} {} {} {} {} {} {}'.format(tm, P[0], P[1], P[2], L[0], L[1], L[2]), file=f_real_m)
        pos = lf.pos
        rpy = lf.getRPY()
        print('{} {} {} {} {} {} {}'.format(tm, pos[0], pos[1], pos[2], rpy[0], rpy[1], rpy[2]), file=f_real_lf)
        pos = rf.pos
        rpy = rf.getRPY()
        print('{} {} {} {} {} {} {}'.format(tm, pos[0], pos[1], pos[2], rpy[0], rpy[1], rpy[2]), file=f_real_rf)
        ## control
        calcLinkMovements(robot, lst_tm, lst_ctrl_pos, lst_ctrl_rot, lst_ctrl_q, index=idx)
        ##
        tm = lst_tm[idx]
        lf = robot.lleg.endEffector
        rf = robot.rleg.endEffector
        P, L = robot.robot.calcTotalMomentum()
        ##
        print('{} {} {} {} {} {} {}'.format(tm, P[0], P[1], P[2], L[0], L[1], L[2]), file=f_ctrl_m)
        pos = lf.pos
        rpy = lf.getRPY()
        print('{} {} {} {} {} {} {}'.format(tm, pos[0], pos[1], pos[2], rpy[0], rpy[1], rpy[2]), file=f_ctrl_lf)
        pos = rf.pos
        rpy = rf.getRPY()
        print('{} {} {} {} {} {} {}'.format(tm, pos[0], pos[1], pos[2], rpy[0], rpy[1], rpy[2]), file=f_ctrl_rf)

    f_real_m.close()
    f_ctrl_m.close()
    f_real_lf.close()
    f_real_rf.close()
    f_ctrl_lf.close()
    f_ctrl_rf.close()
