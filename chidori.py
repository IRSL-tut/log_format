exec(open('/choreonoid_ws/install/share/irsl_choreonoid/sample/irsl_import.py').read())

def setupChidori(modelFile='CHIDORI/model/CHIDORImain.wrl', name = 'CHIDORI'):
    r_ = ru.loadRobotItem(modelFile, name=name)
    mdl_ = RobotModel(r_)
    mdl_.registerEndEffector('rleg', ## end-effector
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
    mdl_.registerEndEffector('lleg', ## end-effector
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
    return mdl_

# robot = setupChidori()
#
### down waist(up foot)
# robot.angleVector(fv(0, 0, 0, 0, 0, 0,  0, 0, 0, 0, 0, 0))
# robot.rleg.move(fv(0.0, 0.0, 0.1))
# robot.lleg.move(fv(0.0, 0.0, 0.1))
# robot.fixLegToCoords(coordinates())
#
### loop for fixing centroid
# robot.fixLegToCoords(coordinates())
# robot.rleg.move(fv(0.005, 0, 0))
# robot.lleg.move(fv(0.005, 0, 0))
# robot.centroid -> 0 0 xxx
