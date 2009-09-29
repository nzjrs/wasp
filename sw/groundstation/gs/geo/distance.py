import math
import constants

# Taken from
# http://www.movable-type.co.uk/scripts/latlong.html
def distance_haverstine(start, end):
    """
    Use Haversine formula to calculate distance (in km) between two points specified by 
    (latitude,longitude) tuples, in numeric degrees

    Based on Haversine formula (http://en.wikipedia.org/wiki/Haversine_formula).
    Implementation inspired by JavaScript implementation from 
    http://www.movable-type.co.uk/scripts/latlong.html
    """
    lat1,lon1 = start
    lat2,lon2 = end

    r = constants.EARTH_MEAN_RADIUS_KM
    dlat = math.radians(lat2-lat1)
    dlon = math.radians(lon2-lon1)
    a = math.sin(dlat/2.0) * math.sin(dlat/2.0) +                       \
        math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *   \
        math.sin(dlon/2.0) * math.sin(dlon/2.0) 
    c = 2.0 * math.atan2(math.sqrt(a), math.sqrt(1.0-a))
    d = r * c
    return d

# Taken from
# http://www.movable-type.co.uk/scripts/latlong.html
def distance_cosine_law(start, end):
    """
    Use Law of Cosines to calculate distance (in km) between two points specified by 
    (latitude,longitude) tuples, in numeric degrees
    """
    lat1,lon1 = start
    lat2,lon2 = end

    r = constants.EARTH_MEAN_RADIUS_KM
    d = math.acos(math.sin(math.radians(lat1))*math.sin(math.radians(lat2)) +   \
        math.cos(math.radians(lat1))*math.cos(math.radians(lat2))*math.cos(math.radians(lon2-lon1))) * r
    return d

# Taken from pyroms
# http://pyroms.googlecode.com/svn/trunk/pyroms/greatcircle.py
def distance_vinchey(f, a, start, end):
        """ 
        Uses Vincenty formula for distance between two Latitude/Longitude points
        (latitude,longitude) tuples, in numeric degrees. f,a are ellipsoidal parameters

        Returns the distance (m) between two geographic points on the ellipsoid and the 
        forward and reverse azimuths between these points. Returns ( s, alpha12,  alpha21 ) as a tuple
        """

        # Convert into notation from the original paper
        # http://www.anzlic.org.au/icsm/gdatum/chapter4.html
        #
        # Vincenty's Inverse formulae
        # Given: latitude and longitude of two points (phi1, lembda1 and phi2, lembda2)
        phi1 = math.radians(start[0]); lembda1 = math.radians(start[1]);
        phi2 = math.radians(end[0]); lembda2 = math.radians(end[1]);

        if (abs( phi2 - phi1 ) < 1e-8) and ( abs( lembda2 - lembda1) < 1e-8 ):
          return 0.0, 0.0, 0.0
  
        two_pi = 2.0*math.pi

        b = a * (1.0 - f)

        TanU1 = (1-f) * math.tan( phi1 )
        TanU2 = (1-f) * math.tan( phi2 )
        
        U1 = math.atan(TanU1)
        U2 = math.atan(TanU2)

        lembda = lembda2 - lembda1
        last_lembda = -4000000.0                # an impossibe value
        omega = lembda

        # Iterate the following equations,  until there is no significant change in lembda 
        while ( last_lembda < -3000000.0 or lembda != 0 and abs( (last_lembda - lembda)/lembda) > 1.0e-9 ) :
            sqr_sin_sigma = pow( math.cos(U2) * math.sin(lembda), 2) + \
                pow( (math.cos(U1) * math.sin(U2) - \
                math.sin(U1) *  math.cos(U2) * math.cos(lembda) ), 2 )

            Sin_sigma = math.sqrt( sqr_sin_sigma )
            Cos_sigma = math.sin(U1) * math.sin(U2) + math.cos(U1) * math.cos(U2) * math.cos(lembda)
            sigma = math.atan2( Sin_sigma, Cos_sigma )
            Sin_alpha = math.cos(U1) * math.cos(U2) * math.sin(lembda) / math.sin(sigma)
            alpha = math.asin( Sin_alpha )
            Cos2sigma_m = math.cos(sigma) - (2 * math.sin(U1) * math.sin(U2) / pow(math.cos(alpha), 2) )
            C = (f/16) * pow(math.cos(alpha), 2) * (4 + f * (4 - 3 * pow(math.cos(alpha), 2)))
            last_lembda = lembda
            lembda = omega + (1-C) * f * math.sin(alpha) * (sigma + C * math.sin(sigma) * \
                (Cos2sigma_m + C * math.cos(sigma) * (-1 + 2 * pow(Cos2sigma_m, 2) )))
        
        u2 = pow(math.cos(alpha),2) * (a*a-b*b) / (b*b)
        A = 1 + (u2/16384) * (4096 + u2 * (-768 + u2 * (320 - 175 * u2)))
        B = (u2/1024) * (256 + u2 * (-128+ u2 * (74 - 47 * u2)))
        delta_sigma = B * Sin_sigma * (Cos2sigma_m + (B/4) * \
                (Cos_sigma * (-1 + 2 * pow(Cos2sigma_m, 2) ) - \
                (B/6) * Cos2sigma_m * (-3 + 4 * sqr_sin_sigma) * \
                (-3 + 4 * pow(Cos2sigma_m,2 ) )))
        
        s = b * A * (sigma - delta_sigma)
        
        alpha12 = math.atan2( (math.cos(U2) * math.sin(lembda)), \
                (math.cos(U1) * math.sin(U2) - math.sin(U1) * math.cos(U2) * math.cos(lembda)))
        
        alpha21 = math.atan2( (math.cos(U1) * math.sin(lembda)), \
                (-math.sin(U1) * math.cos(U2) + math.cos(U1) * math.sin(U2) * math.cos(lembda)))

        if ( alpha12 < 0.0 ) : 
                alpha12 =  alpha12 + two_pi
        if ( alpha12 > two_pi ) : 
                alpha12 = alpha12 - two_pi

        alpha21 = alpha21 + two_pi / 2.0
        if ( alpha21 < 0.0 ) : 
                alpha21 = alpha21 + two_pi
        if ( alpha21 > two_pi ) : 
                alpha21 = alpha21 - two_pi

        return s, alpha12,  alpha21 

