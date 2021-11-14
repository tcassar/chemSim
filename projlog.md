Date:   Sun Nov 14 20:04:30 2021 +0000

    changed coef of rest. to make funky graphs. Add eqm values to graphs. Plot time vs dist, energy, force. Have a nice sample csv and log to show tomorrow

Date:   Sun Nov 14 19:20:09 2021 +0000

    Full CLI; working very nicely; graph accepts stdin or file with -f | --file flag

Date:   Sun Nov 14 18:55:56 2021 +0000

    Realised force was being converted to nanonewtons during run, not just output - fixed this. Realised eq for force was wrong. Also fixed, miracle was working well before. 0.3s of motion were simulated, with error of 0.005%. Added samples to beused tomorrow if things go south

Date:   Sun Nov 14 15:38:27 2021 +0000

    add helps to cli args

Date:   Sun Nov 14 14:32:36 2021 +0000

    write CLI for prog

Date:   Sun Nov 14 11:03:14 2021 +0000

    Program safely quits with keyboard interrupt, including report

Date:   Sat Nov 13 17:59:04 2021 +0000

    redirect data to STDOUT, logs to STDERR

Date:   Sat Nov 13 17:44:36 2021 +0000

    logs to log files, outputs to csv files for much graphable data

Date:   Thu Nov 11 13:55:10 2021 +0000

    rm __pycache__ from working

Date:   Thu Nov 11 09:50:36 2021 +0000

    Changes getter methods to just use attributes. Currently set up with poor logging but works to file

Date:   Thu Nov 11 09:45:34 2021 +0000

    Restructure energetics tests to ensure tests are completely isolated (i.e. new objects generated every unittest)

Date:   Wed Nov 10 11:10:14 2021 +0000

    Adds constant acceleration test; passes

Date:   Tue Nov 9 15:19:51 2021 +0000

    Seems to hover around average expected seperation

Date:   Mon Nov 8 22:04:03 2021 +0000

    Verifies energetics for when r=sigma and distance where force = 0

Date:   Mon Nov 8 11:21:07 2021 +0000

    Energetics Test is written and passing

Date:   Mon Nov 8 09:05:15 2021 +0000

    has a cycle, not really doing well on average distance

Date:   Sun Nov 7 17:42:27 2021 +0000

    Update hashing of potentials - would have produced many collisions before. Now concat IDs of atoms and hash resulting str

Date:   Fri Oct 29 15:41:25 2021 +0100

    Update README

Date:   Wed Oct 27 14:57:00 2021 +0100

    Three atoms seems to work. Desperatr need of visualiser

Date:   Wed Oct 27 14:10:44 2021 +0100

    Preps what is needed for an n atom sim. Potential now calls Atom's accumulator method as opposed to move. Accumulator allows multiple potentials to add force. Simulation frames computed by calling individually each atoms .move() function

Date:   Wed Oct 27 12:37:52 2021 +0100

    adds helper func for atoms, which returns ID as str

Date:   Wed Oct 27 12:36:39 2021 +0100

    combined hash of two atoms (through x.update()) is equal to hash of potential. Allows easy check if potential has spawned."

Date:   Thu Oct 21 14:49:59 2021 +0100

    Makes potential hashable, and can be stored in hash maps. Hash based off bytes of repr of atm1 and atm2 in potential

Date:   Thu Oct 21 13:21:24 2021 +0100

    Change structure of working dir. Deleted old stuff permanently, now only 1D sim (2D coming soon). Collision detection with walls seems functional, leave for now. Ought to write some tests

Date:   Wed Oct 20 00:05:06 2021 +0100

    Repo clearup after vm tomfoolery. Containers seem to be containing particles, which is nice

Date:   Mon Oct 18 18:58:03 2021 +0100

    for switching VMs

Date:   Fri Oct 15 12:11:41 2021 +0100

    Changes way distance is evaluated, so only calculated once per cycle

Date:   Tue Oct 12 21:13:48 2021 +0100

    Allows time to be controlled by Potential, can be varied between frames

Date:   Tue Oct 12 20:21:19 2021 +0100

    renames v2/ to one_dimension/

Date:   Tue Oct 12 20:04:44 2021 +0100

    Lots of things. Project log got updated. Main change is v2/ folder (needs renaming). Does accurate 2 atom 1 dimension simulation. Next commit needs to generalise setup (i.e. time per frame needs to be in one place.

Date:   Mon Oct 4 20:57:55 2021 +0100

    Restructure filesystem; adds tests folder, gives src an __init__.py file. Removes viz

Date:   Tue Sep 21 07:56:34 2021 +0100

    Two atoms seem to be working, need to integration test

Date:   Tue Sep 21 07:44:24 2021 +0100

    rewrite trig tests to be better

Date:   Tue Sep 21 07:36:53 2021 +0100

    trig funcs and tests

Date:   Tue Sep 21 06:53:15 2021 +0100

    Add inaccurate atan method j for development to  work with decimal, probably not accurate enough for real thing. Changes documentation

Date:   Sun Sep 5 13:55:54 2021 +0100

    Delete temp.py~

Date:   Sun Sep 5 11:53:25 2021 +0100

    changed values in test_staged_motion to be correct (had not realised change in origin before, hence values were wrong

Date:   Sun Sep 5 11:45:02 2021 +0100

    Fixes problem with incorrect displacement, fixed reversible test problem (i.e. applying a force then the -ve of the force does not return you to origin), wrote test to monitor constant acceleration

Date:   Fri Sep 3 23:55:46 2021 +0100

    adds plan folder

Date:   Fri Sep 3 23:54:47 2021 +0100

    Removed integral test that was causing problems, added tests that check atom moves correctly against hand verified data, and a test to make sure when fed data *= -1, atom returns to inital state (doesnt atm)

Date:   Thu Sep 2 18:46:54 2021 +0100

    maia

Date:   Mon Aug 30 16:46:53 2021 +0100

    Same as last msg

Date:   Mon Aug 30 16:46:23 2021 +0100

    Tests atom moves from standing as it should. Had to update kinematics, and fixed a problem wherein atomic mass was not in reduced units

Date:   Thu Aug 26 13:20:31 2021 +0100

    Updated so now has capacity to cycle from state n to state n+1. Am dubious as to the fact that kinematics is correct. Next step is write unit tests to check kinematics. Viz also needs writing

Date:   Sun Aug 15 00:27:18 2021 +0100

    First stage of basic two molecule implementation. Only configured to work with Ar-Ar interaction. Calculates interatomic distance based off positions of each atom, can calculate interatomic potential via LJ.

Date:   Fri Aug 13 16:18:17 2021 +0100

    PLAN: First draft of Initial Project Review log. Requires some later changes, updates w missing info

Date:   Mon May 10 21:33:11 2021 +0100

    Update log, brief dev plan, brief requirements

Date:   Mon May 10 09:43:30 2021 +0100

    Updates requirements, adds planning folder for me to keep track of what's going on. Log file in /planning/ is md, not program logs

Date:   Sun May 9 22:58:42 2021 +0100

    Basic script to plot a LJ Potential, very minimal functionality.

Date:   Sat Apr 24 13:13:56 2021 +0100

    initial commit
