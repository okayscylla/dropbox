from dotenv import load_dotenv
import os

load_dotenv()

def access_secret():
    return os.getenv("DBX_KEY")

def bad_secret(): # TODO generate this
    return "sl.B98fvKZy8KTwGqiGLmGQUNXT6HcNFm2U4_VpMTvYwfl5lFpaCxli8zA9eWV9ugNnnwpm2Pj5mm5TElIPqiRGDVZZSSlEye5NG2tuMaWBTQSjQMWRsMzYmcG-BOJdYesnnMBJ33f6zOFS"


if __name__ == "__main__":
    print(access_secret())
    print(bad_secret())