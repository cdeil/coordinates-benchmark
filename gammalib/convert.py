"""
Coordinate conversions with the gammalib C++ / Python package.

http://gammalib.sourceforge.net
"""
import numpy as np
import gammalib

SUPPORTED_SYSTEMS = 'fk4 fk5 icrs galactic'.split()

def convert(coords, systems):

    if not set(systems.values()).issubset(SUPPORTED_SYSTEMS):
        return None

    lons = np.zeros_like(coords['lon'])
    lats = np.zeros_like(coords['lat'])

    for ii, (lon, lat) in enumerate(zip(coords['lon'], coords['lat'])):
        sky_dir = gammalib.GSkyDir()

        if systems['in'] in ['fk4', 'fk5', 'icrs']:
            sky_dir.radec_deg(lon, lat)
        elif systems['in'] == 'galactic':
            sky_dir.lb_deg(lon, lat)

        if systems['in'] in ['fk4', 'fk5', 'icrs']:
            lon, lat = sky_dir.ra_deg(), sky_dir.dec_deg()
        elif systems['in'] == 'galactic':
            lon, lat = sky_dir.l_deg(), sky_dir.b_deg()

        # Wrap longitude to range 0 to 360
        #lon = np.where(lon < 0, lon + 360, lon) 

        lons[ii], lats[ii] = lon, lat

    return dict(lon=lons, lat=lats)
