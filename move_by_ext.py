def find_and_process(args, count=0, log=""):
    """Find the files by file extension and process (move/copy/remove) them."""

    def process(the_path, the_file):
        """Process each file."""
        processed = 0
        src_file = os.path.join(the_path, the_file)
        dst_file = os.path.join(args.dst, the_file)
        if args.rm:
            os.remove(src_file)
            processed = 1
        else:
            if not os.path.exists(dst_file): # not replace if already exists 
                if args.cp:
                    shutil.copy2(src_file, dst_file)
                else:
                    shutil.move(src_file, dst_file)
                processed = 1
        return processed

    if not os.path.exists(args.dst):
        os.mkdir(args.dst)
    for path, directories, files in os.walk(args.src):
        for fil in files:
            # ignore files without extension (can have the same name as the ext)
            file_ext = fil.split('.')[-1] if len(fil.split('.')) > 1 else None
            # ignore dots in given extensions
            extensions = [ext.replace('.', '') for ext in args.ext]
            if file_ext in extensions:
                count += process(path, fil)

    opt = int("{0}{1}".format(int(args.rm), int(args.cp)), 2)
    log = "Files {0}: {1}".format({0:"moved", 1:"copied", 2:"removed"}[opt], count)
    return log
