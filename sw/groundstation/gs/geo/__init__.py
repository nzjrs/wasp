import distance
import constants

def crow_flies_distance_two_point(start, end, method="haverstine"):
    """
    @returns the crow flies distance between the two points in meters
    """
    if method == "haverstine":
        return distance.distance_haverstine(start, end) * 1000.0
    elif method == "cosine":
        return distance.distance_cosine_law(start, end) * 1000.0
    elif method == "vinchey":
        a,b = constants.ELLIPSOID["WGS84"]
        f = (a-b)/a
        dist, alpha12, alpha21 = distance.distance_vinchey(f, a, start, end)
        return dist
    else:
        raise ValueError("Method must be one of haverstine,cosine,vinchey")

if __name__ == '__main__':
    #co-ordinates from
    #http://www.travelmath.com/airport/LAX
    #http://www.travelmath.com/airport/BNA
    lax = (33.9425222, -118.4071611)
    bna = (36.12666666, -86.68194444)

    #co-ordinates from
    #http://pyroms.googlecode.com/svn/trunk/pyroms/greatcircle.py
    #ellipsoidal distance should be 54972.271m
    flinders_peak = (-37.951033, 144.424868)
    buninyon = (-37.652821, 143.926496)

    for start,end,n in ((lax, bna, "lax->bna"), (flinders_peak, buninyon, "flinders peak->buninyon")):
        print n, ": distance haverstine (m)", crow_flies_distance_two_point(start, end, "haverstine")
        print n, ": distance cosine law (m)", crow_flies_distance_two_point(start, end, "cosine")
        print n, ": distance vinchey (m)", crow_flies_distance_two_point(start, end, "vinchey")
