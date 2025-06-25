import copy
import opsc
import oobb
import oobb_base
import yaml
import os
import scad_help

def main(**kwargs):
    make_scad(**kwargs)

def make_scad(**kwargs):
    parts = []

    typ = kwargs.get("typ", "")

    if typ == "":
        #setup    
        #typ = "all"
        typ = "fast"
        #typ = "manual"

    oomp_mode = "project"
    #oomp_mode = "oobb"

    test = False
    #test = True

    if typ == "all":
        filter = ""; save_type = "all"; navigation = True; overwrite = True; modes = ["3dpr"]; oomp_run = True; test = False
        #default
        #filter = ""; save_type = "all"; navigation = True; overwrite = True; modes = ["3dpr"]; oomp_run = True; test = False
    elif typ == "fast":
        filter = ""; save_type = "none"; navigation = False; overwrite = True; modes = ["3dpr"]; oomp_run = False
        #default
        #filter = ""; save_type = "none"; navigation = False; overwrite = True; modes = ["3dpr"]; oomp_run = False
    elif typ == "manual":
    #filter
        filter = ""
        #filter = "test"

    #save_type
        save_type = "none"
        #save_type = "all"
        
    #navigation        
        #navigation = False
        navigation = True    

    #overwrite
        overwrite = True
                
    #modes
        #modes = ["3dpr", "laser", "true"]
        modes = ["3dpr"]
        #modes = ["laser"]    

    #oomp_run
        oomp_run = True
        #oomp_run = False    

    #adding to kwargs
    kwargs["filter"] = filter
    kwargs["save_type"] = save_type
    kwargs["navigation"] = navigation
    kwargs["overwrite"] = overwrite
    kwargs["modes"] = modes
    kwargs["oomp_mode"] = oomp_mode
    kwargs["oomp_run"] = oomp_run
    
       
    # project_variables
    if True:
        pass
    
    # declare parts
    if True:

        directory_name = os.path.dirname(__file__) 
        directory_name = directory_name.replace("/", "\\")
        project_name = directory_name.split("\\")[-1]
        #max 60 characters
        length_max = 40
        if len(project_name) > length_max:
            project_name = project_name[:length_max]
            #if ends with a _ remove it 
            if project_name[-1] == "_":
                project_name = project_name[:-1]
                
        #defaults
        kwargs["size"] = "oobb"
        kwargs["width"] = 1
        kwargs["height"] = 1
        kwargs["thickness"] = 3
        #oomp_bits
        if oomp_mode == "project":
            kwargs["oomp_classification"] = "project"
            kwargs["oomp_type"] = "github"
            kwargs["oomp_size"] = "oomlout"
            kwargs["oomp_color"] = project_name
            kwargs["oomp_description_main"] = ""
            kwargs["oomp_description_extra"] = ""
            kwargs["oomp_manufacturer"] = ""
            kwargs["oomp_part_number"] = ""
        elif oomp_mode == "oobb":
            kwargs["oomp_classification"] = "oobb"
            kwargs["oomp_type"] = "part"
            kwargs["oomp_size"] = ""
            kwargs["oomp_color"] = ""
            kwargs["oomp_description_main"] = ""
            kwargs["oomp_description_extra"] = ""
            kwargs["oomp_manufacturer"] = ""
            kwargs["oomp_part_number"] = ""

        part_default = {} 
       
        part_default["project_name"] = project_name
        part_default["full_shift"] = [0, 0, 0]
        part_default["full_rotations"] = [0, 0, 0]
        
        names = []
        #names.append("version_1")
        #names.append("version_2")
        names.append("version_3")

        extras = []
        extras.append("")
        extras.append("base_only")
        extras.append("lifter_only")

        sizes = []
        sizes.append([9,14])
        sizes.append([11,12]) #version 2
        sizes.append([11,11]) #version 2

        for nam in names:
            for ex in extras:
                for siz in sizes:
                    part = copy.deepcopy(part_default)
                    p3 = copy.deepcopy(kwargs)
                    p3["width"] = siz[0]
                    p3["height"] = siz[1]
                    p3["thickness"] = 24
                    if ex != "":    
                        p3["extra"] = ex
                    part["kwargs"] = p3
                    #nam = "version_1"
                    part["name"] = nam
                    if oomp_mode == "oobb":
                        p3["oomp_size"] = nam
                    if not test:
                        pass
                        parts.append(part)


    kwargs["parts"] = parts

    scad_help.make_parts(**kwargs)

    #generate navigation
    if navigation:
        sort = []
        
        sort.append("name")
        sort.append("width")
        sort.append("height")
        sort.append("thickness")
        sort.append("extra")
        
        scad_help.generate_navigation(sort = sort)

def get_version_3(thing, **kwargs):
    import math
    prepare_print = kwargs.get("prepare_print", False)
    width = kwargs.get("width", 1)
    width_mm = (width * 15)-1
    height = kwargs.get("height", 1)
    height_mm = (height * 15)-1
    depth = kwargs.get("thickness", 3)                    
    rot = kwargs.get("rot", [0, 0, 0])
    pos = kwargs.get("pos", [0, 0, 0])
    extra = kwargs.get("extra", "")
    

    positions = []
    positions.append([1, 1])
    positions.append([1, height])
    positions.append([width, 1])
    positions.append([width, height])
    positions.append([(width+1)/2, 1])
    positions.append([(width)-2, 1])
    positions.append([3, 1])
    up_shift = 4
    positions.append([1, up_shift])
    positions.append([width, up_shift])
    up_shift_2 = 8
    positions.append([1, up_shift_2])
    positions.append([width, up_shift_2])

    

    #add base
    if "lifter_only" not in extra:
        p3 = copy.deepcopy(kwargs)
        p3["type"] = "positive"
        p3["shape"] = f"oobb_plate"    
        p3["width"] = width
        p3["height"] = 1
        p3["depth"] = 3
        #p3["holes"] = True         uncomment to include default holes
        #p3["m"] = "#"
        pos1 = copy.deepcopy(pos)         
        poss = []
        pos11 = copy.deepcopy(pos1)
        pos11[1] += (height-1)/2*15
        poss.append(pos11)
        pos12 = copy.deepcopy(pos1)
        pos12[1] += -(height-1)/2*15
        poss.append(pos12)

        p3["pos"] = poss
        oobb_base.append_full(thing,**p3)

        #add back piece
        p3 = copy.deepcopy(kwargs)
        p3["type"] = "positive"
        p3["shape"] = f"oobb_plate"
        p3["depth"] = 3
        p3["width"] = 1
        p3["height"] = height
        #p3["holes"] = True         uncomment to include default holes
        #p3["m"] = "#"
        pos1 = copy.deepcopy(pos)
        pos1[0] += 0
        poss   = []
        pos11 = copy.deepcopy(pos1)
        pos11[0] += (width-1)/2 * 15
        poss.append(pos11)
        pos12 = copy.deepcopy(pos1)
        pos12[0] += -(width-1)/2 * 15
        poss.append(pos12)
        p3["pos"] = poss
        oobb_base.append_full(thing,**p3)

        #add crosses
        length_hypotenuse = math.sqrt(width_mm**2 + height_mm**2) - 10
        angle = math.degrees(math.atan(height_mm/width_mm))
        p3 = copy.deepcopy(kwargs)
        p3["type"] = "positive"
        p3["shape"] = f"rounded_rectangle"
        dep = 3
        wid = 14
        hei = length_hypotenuse
        size = [wid, hei, dep]
        p3["size"] = size
        #p3["holes"] = True         uncomment to include default holes
        #p3["m"] = "#"
        #angle = 59.7
        if True:
            p4 = copy.deepcopy(p3)
            rot1 = copy.deepcopy(rot)
            rot1[2] += 90-angle
            p4["rot"] = rot1
            pos1 = copy.deepcopy(pos)
            p4["pos"] = pos1
            oobb_base.append_full(thing,**p4)
        if True:
            p4 = copy.deepcopy(p3)
            rot1 = copy.deepcopy(rot)
            rot1[2] += 90+angle
            p4["rot"] = rot1
            pos1 = copy.deepcopy(pos)
            pos1[0] += 0
            p4["pos"] = pos1
            oobb_base.append_full(thing,**p4)


        


    if True:
        #add holes seperate
        locs = copy.deepcopy(positions)
        locs.append([1, 1])
        locs.append([1, height])
        locs.append([width, 1])
        locs.append([width, height])
        p3 = copy.deepcopy(kwargs)
        p3["type"] = "p"
        p3["shape"] = f"oobb_holes"
        p3["both_holes"] = False  
        p3["depth"] = depth
        p3["holes"] = "single"
        p3["location"] = locs
        #p3["m"] = "#"
        pos1 = copy.deepcopy(pos)         
        p3["pos"] = pos1
        oobb_base.append_full(thing,**p3)
    
    #add lifters
    if "base_only" not in extra:             
        #add top bottom and side plate
        p3 = copy.deepcopy(kwargs)
        p3["type"] = "positive"
        p3["shape"] = f"oobb_plate"
        p3["depth"] = depth
        p3["width"] = 1
        p3["height"] = 1
        #p3["holes"] = True         uncomment to include default holes
        #p3["m"] = "#"
        poss = []
        pos1 = copy.deepcopy(pos)
        pos1[0] += -(width-1)/2*15
        pos1[1] += -(height-1)/2*15 
        for p in positions:
            pos11 = copy.deepcopy(pos1)
            pos11[0] += (p[0]-1) * 15
            pos11[1] += (p[1]-1) * 15
            poss.append(pos11)
        
        p3["pos"] = poss
        oobb_base.append_full(thing,**p3)

def get_version_2(thing, **kwargs):

    prepare_print = kwargs.get("prepare_print", False)
    width = kwargs.get("width", 1)
    height = kwargs.get("height", 1)
    depth = kwargs.get("thickness", 3)                    
    rot = kwargs.get("rot", [0, 0, 0])
    pos = kwargs.get("pos", [0, 0, 0])
    extra = kwargs.get("extra", "")
    

    positions = []
    positions.append([1, 1])
    positions.append([1, height])
    positions.append([width, 1])
    positions.append([width, height])
    positions.append([1, (height+1)/2])
    positions.append([1, height-3])
    positions.append([1, 4])

    #add base
    if "lifter_only" not in extra:
        p3 = copy.deepcopy(kwargs)
        p3["type"] = "positive"
        p3["shape"] = f"oobb_plate"    
        p3["width"] = width
        p3["height"] = 1
        p3["depth"] = 3
        #p3["holes"] = True         uncomment to include default holes
        #p3["m"] = "#"
        pos1 = copy.deepcopy(pos)         
        poss = []
        pos11 = copy.deepcopy(pos1)
        pos11[1] += (height-1)/2*15
        poss.append(pos11)
        pos12 = copy.deepcopy(pos1)
        pos12[1] += -(height-1)/2*15
        poss.append(pos12)

        p3["pos"] = poss
        oobb_base.append_full(thing,**p3)

        #add back piece
        p3 = copy.deepcopy(kwargs)
        p3["type"] = "positive"
        p3["shape"] = f"oobb_plate"
        p3["depth"] = 3
        p3["width"] = 1
        p3["height"] = height
        #p3["holes"] = True         uncomment to include default holes
        #p3["m"] = "#"
        pos1 = copy.deepcopy(pos)
        pos1[0] += 0
        poss   = []
        pos11 = copy.deepcopy(pos1)
        pos11[0] += (width-1)/2 * 15
        poss.append(pos11)
        pos12 = copy.deepcopy(pos1)
        pos12[0] += -(width-1)/2 * 15
        poss.append(pos12)
        p3["pos"] = poss
        oobb_base.append_full(thing,**p3)

        #add crosses
        p3 = copy.deepcopy(kwargs)
        p3["type"] = "positive"
        p3["shape"] = f"rounded_rectangle"
        dep = 3
        wid = 14
        hei = 230
        size = [wid, hei, dep]
        p3["size"] = size
        #p3["holes"] = True         uncomment to include default holes
        #p3["m"] = "#"
        angle = 59.7
        if True:
            p4 = copy.deepcopy(p3)
            rot1 = copy.deepcopy(rot)
            rot1[2] += 90-angle
            p4["rot"] = rot1
            pos1 = copy.deepcopy(pos)
            p4["pos"] = pos1
            oobb_base.append_full(thing,**p4)
        if True:
            p4 = copy.deepcopy(p3)
            rot1 = copy.deepcopy(rot)
            rot1[2] += 90+angle
            p4["rot"] = rot1
            pos1 = copy.deepcopy(pos)
            pos1[0] += 0
            p4["pos"] = pos1
            oobb_base.append_full(thing,**p4)


        


    if True:
        #add holes seperate
        locs = copy.deepcopy(positions)
        locs.append([1, 1])
        locs.append([1, height])
        locs.append([width, 1])
        locs.append([width, height])
        p3 = copy.deepcopy(kwargs)
        p3["type"] = "p"
        p3["shape"] = f"oobb_holes"
        p3["both_holes"] = False  
        p3["depth"] = depth
        p3["holes"] = "single"
        p3["location"] = locs
        #p3["m"] = "#"
        pos1 = copy.deepcopy(pos)         
        p3["pos"] = pos1
        oobb_base.append_full(thing,**p3)
    
    #add lifters
    if "base_only" not in extra:             
        #add top bottom and side plate
        p3 = copy.deepcopy(kwargs)
        p3["type"] = "positive"
        p3["shape"] = f"oobb_plate"
        p3["depth"] = depth
        p3["width"] = 1
        p3["height"] = 1
        #p3["holes"] = True         uncomment to include default holes
        #p3["m"] = "#"
        poss = []
        pos1 = copy.deepcopy(pos)
        pos1[0] += -(width-1)/2*15
        pos1[1] += -(height-1)/2*15 
        for p in positions:
            pos11 = copy.deepcopy(pos1)
            pos11[0] += (p[0]-1) * 15
            pos11[1] += (p[1]-1) * 15
            poss.append(pos11)
        
        p3["pos"] = poss
        oobb_base.append_full(thing,**p3)

        
        

    if prepare_print:
        #put into a rotation object
        components_second = copy.deepcopy(thing["components"])
        return_value_2 = {}
        return_value_2["type"]  = "rotation"
        return_value_2["typetype"]  = "p"
        pos1 = copy.deepcopy(pos)
        pos1[0] += 50
        return_value_2["pos"] = pos1
        return_value_2["rot"] = [180,0,0]
        return_value_2["objects"] = components_second
        
        thing["components"].append(return_value_2)

    
        #add slice # top
        p3 = copy.deepcopy(kwargs)
        p3["type"] = "n"
        p3["shape"] = f"oobb_slice"
        pos1 = copy.deepcopy(pos)
        pos1[0] += -500/2
        pos1[1] += 0
        pos1[2] += -500/2        
        p3["pos"] = pos1
        #p3["m"] = "#"
        oobb_base.append_full(thing,**p3)


def get_version_1(thing, **kwargs):

    prepare_print = kwargs.get("prepare_print", False)
    width = kwargs.get("width", 1)
    height = kwargs.get("height", 1)
    depth = kwargs.get("thickness", 3)                    
    rot = kwargs.get("rot", [0, 0, 0])
    pos = kwargs.get("pos", [0, 0, 0])
    extra = kwargs.get("extra", "")
    
    #add plate
    p3 = copy.deepcopy(kwargs)
    p3["type"] = "positive"
    p3["shape"] = f"oobb_plate"    
    p3["depth"] = 3
    #p3["holes"] = True         uncomment to include default holes
    #p3["m"] = "#"
    pos1 = copy.deepcopy(pos)         
    p3["pos"] = pos1
    oobb_base.append_full(thing,**p3)
    
    #add top bottom and side plate
    p3 = copy.deepcopy(kwargs)
    p3["type"] = "positive"
    p3["shape"] = f"oobb_plate"
    p3["depth"] = depth
    p3["width"] = width
    p3["height"] = 1
    #p3["holes"] = True         uncomment to include default holes
    #p3["m"] = "#"
    poss = []
    pos1 = copy.deepcopy(pos)
    #pos1[2] += depth/2
    pos11 = copy.deepcopy(pos1)
    pos11[1] += (height-1)/2 * 15    
    poss.append(pos11)
    pos12 = copy.deepcopy(pos1)
    pos12[1] += -(height-1)/2 * 15    
    poss.append(pos12)
    p3["pos"] = poss
    oobb_base.append_full(thing,**p3)

    #add back piece
    p3 = copy.deepcopy(kwargs)
    p3["type"] = "positive"
    p3["shape"] = f"oobb_plate"
    p3["depth"] = depth
    p3["width"] = 1
    p3["height"] = height
    #p3["holes"] = True         uncomment to include default holes
    #p3["m"] = "#"
    pos1 = copy.deepcopy(pos)
    pos1[0] += -(width-1)/2 * 15
    p3["pos"] = pos1    
    oobb_base.append_full(thing,**p3)

    #add holes seperate
    p3 = copy.deepcopy(kwargs)
    p3["type"] = "p"
    p3["shape"] = f"oobb_holes"
    p3["both_holes"] = True  
    p3["depth"] = depth
    p3["holes"] = "perimeter"
    #p3["m"] = "#"
    pos1 = copy.deepcopy(pos)         
    p3["pos"] = pos1
    oobb_base.append_full(thing,**p3)

    if prepare_print:
        #put into a rotation object
        components_second = copy.deepcopy(thing["components"])
        return_value_2 = {}
        return_value_2["type"]  = "rotation"
        return_value_2["typetype"]  = "p"
        pos1 = copy.deepcopy(pos)
        pos1[0] += 50
        return_value_2["pos"] = pos1
        return_value_2["rot"] = [180,0,0]
        return_value_2["objects"] = components_second
        
        thing["components"].append(return_value_2)

    
        #add slice # top
        p3 = copy.deepcopy(kwargs)
        p3["type"] = "n"
        p3["shape"] = f"oobb_slice"
        pos1 = copy.deepcopy(pos)
        pos1[0] += -500/2
        pos1[1] += 0
        pos1[2] += -500/2        
        p3["pos"] = pos1
        #p3["m"] = "#"
        oobb_base.append_full(thing,**p3)

if __name__ == '__main__':
    kwargs = {}
    main(**kwargs)