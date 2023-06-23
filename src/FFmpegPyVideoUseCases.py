import FFmpegPyVideo as ffpy

"""
Use Cases for FFmpegPyVideo
"""

if __name__ == '__main__':

    ## case1: zoom in point
    in_file = "/Users/liuzuhao/PycharmProjects/VideoProducer/out/windows_people_resize.jpg"
    out_file = "/Users/liuzuhao/PycharmProjects/VideoProducer/out/windows_people_zoom3.mp4"
    image_size = (1920, 1280)
    z_point = (0,0)  # zoom in position upper left
    z_effect = "zoom+0.002"  # zoom in speed
    time = 5
    ff_cmd_zoom = ffpy.vf_zoom(in_file, out_file,image_size,z_point, z_effect, time)
    # cmd_output = ffpy.cmd_execute(ff_cmd_zoom)
    # print(cmd_output)
    #
    ## case2: zoom in point move from point a to point b
    out_file2 = "/Users/liuzuhao/PycharmProjects/VideoProducer/out/windows_people_zoom_move3.mp4"
    # move from top to bottom
    point_a = (0, 0)  # start position
    point_b = (0, 1280) # end position
    # move from left to right
    # point_a = (0, 0)  # start position
    # point_b = (1920, 0) # end position
    z_multi = 2
    time = 5
    move_speed = 1

    ff_cmd = ffpy.vf_zoom_move(in_file=in_file
                          , out_file=out_file2
                          , out_size=image_size
                          , point_start=point_a
                          , point_end=point_b
                          , z_effect=z_multi
                          , time=time
                          , move_speed=move_speed
                          )
    cmd_output = ffpy.cmd_execute(ff_cmd)
    print(cmd_output)