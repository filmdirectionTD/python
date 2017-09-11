def FilterProjects(projectsList):
    # get uncorrect names from projects list
    filteredList = []
    for project in projectsList:
        if(("DK_LOGO" not in project) and ("DKFX" not in project) and ("DKFX - HOLIDAY" not in project) and ("DKFX_SHOWREEL" not in project) and ("FAQ" not in project) and ("SONY" not in project) and ("TEST" not in project)):
            filteredList.append(project)

    return filteredList


def FilterScenes(scenesList):
    filteredList = []
    for scene in scenesList:
        if(("SBORKA" not in scene) and ("LAYOUT" not in scene) and ("EDIT" not in scene)):
            filteredList.append(scene)

    return filteredList


def FilterShots(shotsList):
    filteredList = []
    for shot in shotsList:
        if (("EXTRA WORKS" not in shot) and ("Extra work" not in shot) and ("Extra" not in shot) and ("Edit" not in shot) and ("EDIT" not in shot)):
            filteredList.append(shot)

    return filteredList

def CheckIfAssetJob(inputString):

    possibleAssetJobNames = ["CONCEPT",
                                "CONCEPT-ART",
                                "CONCEPT ART",
                                "Concept Art",
                                "Concept_Art",
                                "Concept-Art",
                                "Concept Sculpt",
                                "Concept_Sculpt",
                                "Concept-Sculpt",
                                "CONCEPT SCULPT",
                                "CONCEPT-SCULPT",
                                "CONCEPT_SCULPT",
                                "Hair setup",
                                "Hair_setup",
                                "Hair-setup",
                                "HAIR SETUP",
                                "HAIR_SETUP",
                                "HAIR-SETUP",
                                "Groom",
                                "Grooming",
                                "GROOM",
                                "GROOMING",
                                "Modeling",
                                "Modelling",
                                "Model",
                                "MODEL",
                                "MODELING",
                                "MODELLING",
                                "Sculpting",
                                "Sculpt",
                                "SCULPTING",
                                "SCULPT",
                                "Musceles",
                                "Muscele Setup",
                                "Muscele_Setup",
                                "Muscele-Setup",
                                "Muscele setup",
                                "Muscele_setup",
                                "Muscele-setup",
                                "Muscules",
                                "Muscule Setup",
                                "Muscule_Setup",
                                "Muscule-Setup",
                                "Muscule setup",
                                "Muscule_setup",
                                "Muscule-setup",
                                "Muscles",
                                "Muscle Setup",
                                "Muscle_Setup",
                                "Muscle-Setup",
                                "Muscle setup",
                                "Muscle_setup",
                                "Muscle-setup",
                                "MUSCLES",
                                "MUSCLE-SETUP",
                                "MUSCLE_SETUP",
                                "Rigging",
                                "Rig",
                                "RIG",
                                "RIGGING",
                                "Shading",
                                "SHADING",
                                "Shading,Lighting",
                                "Shading, lighting",
                                "Shading_Lighting",
                                "2.06 Shading_Lighting",
                                "Texturing",
                                "Textures",
                                "TEXTURING",
                                "FX",
                                "Scan",
                                "SCAN",
                                "SCANNING"]

    for possibleName in possibleAssetJobNames:
        if(inputString in possibleName):
            isJob = True
            return isJob


def CheckIfJob(inputString):

    possibleJobNames = ["Animation",
                        "ANIMATION",
                        "4.02 Animation",
                        "Animation_DK",
                        "Concept art",
                        "Crowd",
                        "Compositing",
                        "COMPOSITING",
                        "Keying, Cleanup, Rotoscope",
                        "Keying_Cleanup_Rotoscope",
                        "Cleanup/Roto",
                        "Cleanup",
                        "4_Compositing",
                        "6.04 Compositing",
                        "Mattepaint",
                        "MATTEPAINT",
                        "6.02 Mattepaint",
                        "3D Layout",
                        "Layout",
                        "LAYOUT",
                        "3D_Layuot",
                        "3D_Lyout",
                        "1_Layout_Stremousov",
                        "2_Layout",
                        "FX",
                        "LIGHTING",
                        "Lighting",
                        "RENDER",
                        "RENDERING",
                        "Shading/Lighting",
                        "Shading_Lighting",
                        "3_Lighting",
                        "2.06 Shading_Lighting",
                        "Hair setup",
                        "Muscles",
                        "3D Tracking",
                        "3D Traking",
                        "TRACKING",
                        "5.01 3D Tracking"]

    for possibleName in possibleJobNames:
        if(inputString in possibleName):
            isJob = True
            return isJob

def FilterShotJobs(inputJobs):
    # checkedJobs = []
    #
    # for inputJob in inputJobs:
    #     if(CheckIfJob(inputJob)):
    #         checkedJobs.append(inputJob)
    #
    # return checkedJobs

    filteredJobs = []

    for checkedJob in inputJobs:
        if (checkedJob in "Animation ANIMATION 4.02 Animation Animation_DK"):
            jobObjname = "ANIMATION"
            if (not (jobObjname in filteredJobs)):
                filteredJobs.append(jobObjname)

        if (checkedJob in "Concept art Concept_art Concept-art CONCEPT ART CONCEPT_ART CONCEPT-ART"):
            jobObjname = "CONCEPT-ART"
            if (not (jobObjname in filteredJobs)):
                filteredJobs.append(jobObjname)

        if (checkedJob in "Compositing COMPOSITING Keying, Cleanup, Rotoscope Keying_Cleanup_Rotoscope Cleanup/Roto Cleanup 4_Compositing 6.04 Compositing"):
            jobObjname = "COMPOSITING"
            if (not (jobObjname in filteredJobs)):
                filteredJobs.append(jobObjname)

        if (checkedJob in "Crowd"):
            jobObjname = "CROWD"
            if (not (jobObjname in filteredJobs)):
                filteredJobs.append(jobObjname)

        if (checkedJob in "FX"):
            jobObjname = "FX"
            if (not (jobObjname in filteredJobs)):
                filteredJobs.append(jobObjname)

        if (checkedJob in "3D Layout Layout LAYOUT 3D_Layuot 3D_Lyout 1_Layout_Stremousov 2_Layout"):
            jobObjname = "LAYOUT"
            if (not (jobObjname in filteredJobs)):
                filteredJobs.append(jobObjname)

        if (checkedJob in "LIGHTING Lighting RENDER RENDERING Shading/Lighting Shading_Lighting 3_Lighting 2.06 Shading_Lighting"):
            jobObjname = "LIGHTING"
            if (not (jobObjname in filteredJobs)):
                filteredJobs.append(jobObjname)

        if (checkedJob in "Hair setup"):
            jobObjname = "HAIR-SETUP"
            if (not (jobObjname in filteredJobs)):
                filteredJobs.append(jobObjname)

        if (checkedJob in "Mattepaint MATTEPAINT 6.02 Mattepaint"):
            jobObjname = "MATTEPAINT"
            if (not (jobObjname in filteredJobs)):
                filteredJobs.append(jobObjname)

        if (checkedJob in "Muscles"):
            jobObjname = "MUSCLES"
            if (not (jobObjname in filteredJobs)):
                filteredJobs.append(jobObjname)

        if (checkedJob in "3D Tracking 3D Traking TRACKING 5.01 3D Tracking"):
            jobObjname = "TRACKING"
            if (not (jobObjname in filteredJobs)):
                filteredJobs.append(jobObjname)

    return filteredJobs