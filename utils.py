def access_secret():
    with open("secrets.txt", "r") as f:
        return f.read()

def bad_secret():
    return "sl.B98fvKZy8KTwGqiGLmGQUNXT6HcNFm2U4_VpMTvYwfl5lFpaCxli8zA9eWV9ugNnnwpm2Pj5mm5TElIPqiRGDVZZSSlEye5NG2tuMaWBTQSjQMWRsMzYmcG-BOJdYesnnMBJ33f6zOFS"


if __name__ == "__main__":
    print(access_secret())
    print(bad_secret())