# import cnoid.BodyPlugin
# import cnoid.Body
# import numpy
#jupyter console --kernel=choreonoid

filedir='logs/mc-control-BaselineWalkingController-2024-03-22-15-56-44'
prefix='mc-control-BaselineWalkingController-2024-03-22-15-56-44'

cnoid_log_file='{}/cnoid.log'.format(filedir)
## file check
tmfile='{}/{}.FootManager'.format(filedir, prefix)
## file check
tm_offset=1.3   ## ??
x_offset=0.04   ## initial offset in simulation
y_offset=0.0042 ## initial offset in simulation

exec(open('/choreonoid_ws/install/share/irsl_choreonoid/sample/irsl_import.py').read())

#pm=cnoid.Base.ProjectManager.instance
pm=cbase.ProjectManager.instance
pm.loadProject('logtest.cnoid')

#rootI=cnoid.Base.RootItem.instance
rootI=cbase.RootItem.instance

chidori=rootI.findItem('CHIDORI')
log=rootI.findItem('WorldLogFile')

log.setLogFile(cnoid_log_file)

tmlst = []
with open(tmfile) as f:
    ln = f.readline()
    while ln:
        data=ln.split(' ')
        tmlst.append( float(data[0]) )
        ln = f.readline()

print('Time steps : {}'.format(len(tmlst)))

f_angleVector = open('{}/{}.GT_angles'.format(filedir, prefix), mode='w')
f_rootPos     = open('{}/{}.GT_rootPos'.format(filedir, prefix), mode='w')
f_CoM         = open('{}/{}.GT_com'.format(filedir, prefix), mode='w')
f_rfoot       = open('{}/{}.GT_rfoot_pos'.format(filedir, prefix), mode='w')
f_lfoot       = open('{}/{}.GT_lfoot_pos'.format(filedir, prefix), mode='w')
f_rbush       = open('{}/{}.GT_rfoot_bush_diff'.format(filedir, prefix), mode='w')
f_lbush       = open('{}/{}.GT_lfoot_bush_diff'.format(filedir, prefix), mode='w')
f_rbush_org   = open('{}/{}.GT_rfoot_bush_org'.format(filedir, prefix), mode='w')
f_lbush_org   = open('{}/{}.GT_lfoot_bush_org'.format(filedir, prefix), mode='w')

joints = chidori.body.joints

lroot = chidori.body.rootLink

rleg_base = chidori.body.link('RLEG_JOINT5')
rleg_foot = chidori.body.link('RLEG_BUSH_PITCH')

lleg_base = chidori.body.link('LLEG_JOINT5')
lleg_foot = chidori.body.link('LLEG_BUSH_PITCH')

for tm in tmlst:
    log.recallStateAtTime(tm + tm_offset)
    ##angles
    f_angleVector.write(str(tm))
    for j in joints:
        f_angleVector.write(' ')
        f_angleVector.write(str(j.q))
    f_angleVector.write('\n')
    ## Root
    cds = coordinates(lroot.T)
    pp  = cds.pos
    rpy = cds.getRPY()
    print('{} {} {} {} {} {} {}'.format(tm, pp[0] + x_offset, pp[1] + y_offset, pp[2], rpy[0], rpy[1], rpy[2]), file=f_rootPos)
    ## com
    com = chidori.getCenterOfMass()
    print('{} {} {} {}'.format(tm, com[0] + x_offset, com[1] + y_offset, com[2]), file=f_CoM)
    ## RLEG_foot
    cds = coordinates(rleg_foot.T)
    pp  = cds.pos
    rpy = cds.getRPY()
    print('{} {} {} {} {} {} {}'.format(tm, pp[0] + x_offset, pp[1] + y_offset, pp[2], rpy[0], rpy[1], rpy[2]), file=f_rfoot)
    ## RLEG_bush
    bcs = coordinates(rleg_base.T)
    pp  = bcs.pos
    rpy = bcs.getRPY()
    print('{} {} {} {} {} {} {}'.format(tm, pp[0] + x_offset, pp[1] + y_offset, pp[2], rpy[0], rpy[1], rpy[2]), file=f_rbush_org)
    #bcs.translate(fv(0, 0, -0.04))
    cds = cds.transformation(bcs)
    pp  = cds.pos
    rpy = cds.getRPY()
    print('{} {} {} {} {} {} {}'.format(tm, pp[0], pp[1], pp[2], rpy[0], rpy[1], rpy[2]), file=f_rbush)
    ## LLEG_foot
    cds = coordinates(lleg_foot.T)
    pp  = cds.pos
    rpy = cds.getRPY()
    print('{} {} {} {} {} {} {}'.format(tm, pp[0] + x_offset, pp[1] + y_offset, pp[2], rpy[0], rpy[1], rpy[2]), file=f_lfoot)
    ## LLEG_bush
    bcs = coordinates(lleg_base.T)
    pp  = bcs.pos
    rpy = bcs.getRPY()
    print('{} {} {} {} {} {} {}'.format(tm, pp[0] + x_offset, pp[1] + y_offset, pp[2], rpy[0], rpy[1], rpy[2]), file=f_lbush_org)
    #bcs.translate(fv(0, 0, -0.04))
    cds = cds.transformation(bcs)
    pp  = cds.pos
    rpy = cds.getRPY()
    print('{} {} {} {} {} {} {}'.format(tm, pp[0], pp[1], pp[2], rpy[0], rpy[1], rpy[2]), file=f_lbush)

## close
f_angleVector.close()
f_rootPos.close()
f_CoM.close()
f_lfoot.close()
f_rfoot.close()
f_lbush.close()
f_rbush.close()

