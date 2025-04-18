


exec(open("./dtools.py").read()) # utilities package


root_ = os.getcwd()
dataloc = root_+'/datafiles'

        
###----------------------------------------------------------###
# General rules/style 
# each spiral model function should contain: 
#
#
#
#
#
#
#
###----------------------------------------------------------###


class spiral_eloisa(object):
    """Class representing spiral arm model from Poggio et al. 2021 (EDR3 OB stars)
    
    Attributes
    ----------
    loc : str
        Path to data directory
    arms : np.array
        Array of available arm names
    armcolour : dict
        Color mapping for arms
    Methods
    -------
    getarmlist()
        Initialize arm names and colors
    info()
        Print basic model information
    output_(coordsys='HC')
        Generate spiral arm contours in specified coordinate system
    """
    def __init__(self):
        """
        Initialize the Poggio 2021 spiral arm model with heliocentric configuration.

        Parameters
        ----------
        dataloc : str
            Path to the base data directory.
        """
        self.loc = dataloc + '/Poggio_OB_EDR3'
        self.getarmlist()

    def getarmlist(self):
        """
        Initialize the list of available spiral arms and their corresponding plot colors.
        """
        self.arms = np.array(['all'])
        self.armcolour = {'all': 'black'}

    def info(self):
        """
        Print basic information about the available spiral arms.
        """
        print('')
        print('------------------------')
        dfmodlist = pd.DataFrame(self.arms, columns=['Arm list'])
        print(dfmodlist)
        print('------------------------')

    def output_(self, coordsys='HC'):
        """
        Generate and display spiral arm density contours from OB star data.

        Parameters
        ----------
        coordsys : str, optional
            Coordinate system: 'HC' (heliocentric) or 'GC' (galactocentric).
         """
        xcorr = 0.0
        xsun = self.xsun
        if coordsys == 'GC':
            xcorr = xsun

        print(xsun)
        print(xcorr)
        print(coordsys)

        # #read overdensity contours
        xvalues_overdens = np.load(self.loc + '/xvalues_dens.npy')
        yvalues_overdens = np.load(self.loc + '/yvalues_dens.npy')
        over_dens_grid = np.load(self.loc + '/over_dens_grid_threshold_0_003_dens.npy')
        phi1_dens = np.arctan2(yvalues_overdens, -xvalues_overdens)
        Rvalues_dens = sqrtsum(ds=[xvalues_overdens, yvalues_overdens])

        # # #------------------ overplot spiral arms in overdens ------------------
        iniz_overdens = 0  # .1
        fin_overdens = 1.5  # .1
        N_levels_overdens = 2
        levels_overdens = np.linspace(iniz_overdens, fin_overdens, N_levels_overdens)
        # cset1 = plt.contourf(xvalues_overdens + xcorr, yvalues_overdens, over_dens_grid.T, levels=levels_overdens, alpha=0.2, cmap='Greys')
        cset1 = plt.contourf(xvalues_overdens + xcorr, yvalues_overdens, over_dens_grid.T, levels=levels_overdens, alpha=0.05, cmap='Greys')
        # cset1 = plt.contourf(phi1_dens, Rvalues_dens, over_dens_grid.T, levels=levels_overdens, alpha=0.2, cmap='Greys')

        iniz_overdens = 0.  # .1
        fin_overdens = 1.5  # .1
        N_levels_overdens = 4  # 7
        levels_overdens = np.linspace(iniz_overdens, fin_overdens, N_levels_overdens)
        # cset1 = plt.contour(xvalues_overdens + xcorr, yvalues_overdens, over_dens_grid.T, levels=levels_overdens, colors='black', linewidths=0.7)
        cset1 = plt.contour(xvalues_overdens + xcorr, yvalues_overdens, over_dens_grid.T, levels=levels_overdens, colors='black', linewidths=0.2)
        # cset1 = plt.contour(phi1_dens, Rvalues_dens, over_dens_grid.T, levels=levels_overdens, colors='black', linewidths=0.7)

        print('')


class TaylorCordesSpiral:
    
    """ Taylor & Cordes (1993) Galactic spiral arm model,	  
    based on radio pulsar observations. The model defines four major spiral arms and 
    provides both Galactocentric and Heliocentric coordinates for the arm segments.

    Attributes
    ----------
    arms : ndarray
        Array of arm identifiers ['Arm1', 'Arm2', 'Arm3', 'Arm4']
    armcolour : dict
        Color mapping for visualization {'Arm1': 'yellow', ...}
    params : dict
        Original parameters from paper (angles in deg, radii in kpc)
    R0 : float
        Solar galactocentric radius (kpc), set from xsun parameter

    Methods
    -------
    info()
        Display basic model information
    model_(arm_name)
        Generate coordinates for specified arm
    plot_arms(coord_system)
        Visualize arms in chosen coordinate system
    output_(arm, typ_)
        Get coordinates in structured format
    """

    
    def __init__(self, R0=8.5):
        """Initialize spiral parameters from Taylor & Cordes (1993)
        
        Parameters
        ----------
        R0 : float, optional
            Initial solar galactocentric radius (kpc), default 8.5
        """		
        self.getarmlist()
        
    def getarmlist(self):
        """Set arm names and colours"""
    
        self.arms = np.array(['Arm1','Arm2','Arm3','Arm4'])
        self.armcolour = {'Arm1':'yellow','Arm2':'green','Arm3':'blue','Arm4':'purple'}
        self.getparams()
    
    
    def info(self):
        
        '''
        here goes basic info for the user about this model
        '''
    
        print('')
        print('------------------------')	
        dfmodlist = pd.DataFrame(self.arms,columns=['Arm list'])
        print(dfmodlist)
        print('------------------------')		
            
      
    def getparams(self):	   
        """Load original spiral parameters from Taylor & Cordes (1993) Table 1.
        
        Sets params dictionary with:
        - theta_deg: Anchor points in galactic longitude (degrees)
        - r_kpc: Corresponding galactocentric radii (kiloparsecs)
        """
    
        self.params = {	'Arm1': {'theta_deg': [164, 200, 240, 280, 290, 315, 330],
                    'r_kpc': [3.53, 3.76, 4.44, 5.24, 5.36, 5.81, 5.81]},
                    
                    'Arm2':{'theta_deg': [63, 120, 160, 200, 220, 250, 288],
                    'r_kpc': [3.76, 4.56, 4.79, 5.70, 6.49, 7.29, 8.20]},
                    
                    'Arm3':{'theta_deg': [52, 120, 170, 180, 200, 220, 252],
                    'r_kpc': [4.90, 6.27, 6.49, 6.95, 8.20, 8.89, 9.57]},
                    
                    'Arm4':{'theta_deg': [20, 70, 100, 160, 180, 200, 223],
                    'r_kpc': [5.92, 7.06, 7.86, 9.68, 10.37, 11.39, 12.08]}					
                                  
                                  
                                  }

    
    def model_(self, arm_name):	
        
        """Generate arm coordinates using cubic spline interpolation.
        
        Parameters
        ----------
        arm_name : str
            Must be one of: 'Arm1', 'Arm2', 'Arm3', 'Arm4'

        Returns
        -------
        tuple
            (x_hc, y_hc, x_gc, y_gc) coordinate arrays where:
            - hc = heliocentric coordinates
            - gc = galactocentric coordinates

        Raises
        ------
        ValueError
            If invalid arm_name is provided
        """	
        
        self.getparams()
        arm_data = self.params[arm_name]
        theta = np.deg2rad(arm_data['theta_deg'])  # Convert to radians
        r = np.array(arm_data['r_kpc'])
    
        # Cubic spline interpolation for smooth curve
        cs = CubicSpline(theta, r)
        theta_fine = np.linspace(min(theta), max(theta), 300)
        r_fine = cs(theta_fine)
    
        # Convert to Cartesian coordinates (Galacto-Centric)
        x_gc = r_fine * np.sin(theta_fine)
        y_gc = -r_fine * np.cos(theta_fine)
        
        # Convert to Heliocentric coordinates
        x_hc = x_gc + self.R0  # Sun at (-R0, 0) in GC
    
        return x_hc, y_gc, x_gc, y_gc
    
    def plot_arms(self, coord_system='HC'):
        """Visualize spiral arms in specified coordinate system.
        
        Parameters
        ----------
        coord_system : {'HC', 'GC'}, default 'HC'
            Coordinate system for visualization:
        Notes
        -----
        Creates matplotlib figure with arms plotted in predefined colors
        """
        plt.figure(figsize=(10, 10))
        frame_label = "Galacto-Centric" if coord_system == 'GC' else "Helio-Centric"
        plt.title(f"Taylor & Cordes (1993) Spiral Arm Model - {frame_label}", fontsize=14)
        plt.grid(True, alpha=0.3)
    
        for arm in self.arms:
            x_hc, y_gc, x_gc, y_gc = self.generate_arm(arm)
            x, y = (x_gc, y_gc) if coord_system == 'GC' else (x_hc, y_hc)
            plt.plot(x, y, color=arm['color'], label=arm['label'])
    
    def output_(self,arm,typ_='cartesian'):	
        
        """Get arm coordinates in structured format.
        
        Parameters
        ----------
        arm : str
            Arm identifier (e.g., 'Arm1')
        typ_ : {'cartesian', 'polar'}, default 'cartesian'
            Output coordinate type

        Returns
        -------
        dict
            Contains coordinate arrays under keys:
            - 'xhc', 'yhc' (heliocentric)
            - 'xgc', 'ygc' (galactocentric)
            - Additional keys for polar coordinates if requested

        Notes
        -----
        Requires prior setting of xsun attribute for coordinate conversion
        """
        
        xsun = self.xsun
        self.R0 = -xsun  # Solar Galactocentric radius (kpc)
                
        if typ_ =='cartesian':
    
            xhc,yhc,xgc,ygc = self.model_(arm);			
    
            self.dout = {'xhc':xhc,
                         'yhc':yhc,
                         'xgc':xgc,
                         'ygc':ygc}	
        
    

class spiral_houhan(object):	
    """Hou & Han (2014) polynomial-logarithmic spiral arm model
    
    Implements the Milky Way spiral structure model from:
    "The spiral structure of the Milky Way from classical Cepheids" (Hou & Han 2014)
    using polynomial-logarithmic spiral functions. Provides 6 major arm segments.

    Attributes
    ----------
    arms : ndarray
        Array of arm names ['Norma', 'Scutum-Centaurus', ...]
    armcolour : dict
        Visualization colors for each arm
    R0 : float
        Solar galactocentric radius (kpc), calculated from xsun
    params : dict
        Spiral parameters from Table 4 of Hou & Han (2014)
    
    Methods
    -------
    info()
        Display available spiral arms
    model_(arm_name)
        Generate coordinates for specified arm
    output_(arm)
        Get structured coordinate data
    """
    
    def __init__(self):
        

        self.getarmlist()

    def getarmlist(self):
        """Initialize arm names and visualization colors.
        
        Sets:
        - arms: List of 6 spiral arm segments
        - armcolour: Color mapping dictionary with hex/RGB values
        """

        self.arms = np.array(['Norma','Scutum-Centaurus','Sagittarius-Carina','Perseus','Local','Outer'])
        self.armcolour = {'Norma':'black','Scutum-Centaurus':'red','Sagittarius-Carina':'green','Perseus':'blue','Local':'purple','Outer':'gold'}
    
    def info(self):
        
        '''
        Prints formatted table of arm names to stdout.
        '''

        print('')
        print('------------------------')	
        dfmodlist = pd.DataFrame(self.arms,columns=['Arm list'])
        print(dfmodlist)
        print('------------------------')		


    def getparams(self):		
        # Taken value from the table 4 from Hou & Han (2014)
        
        """Load spiral parameters from Hou & Han (2014) Table 4.
        
        Returns
        -------
        dict
            Nested dictionary containing for each arm:
            - a, b, c, d: Polynomial coefficients
            - θ_start: Start angle in degrees (Galactic longitude)
            - θ_end: End angle in degrees
            
        Example
        -------
        >>> params['Scutum-Centaurus']
        {'a': 5.8002, 'b': -1.8188, 'c': 0.2352, 'd': -0.008999,
         'θ_start': 275, 'θ_end': 620}
        """

        
        params = {
            'Norma': {'a': 1.1668, 'b': 0.1198, 'c': 0.002557, 'd': 0.0, 'θ_start': 40, 'θ_end': 250},
            'Scutum-Centaurus': {'a': 5.8002, 'b': -1.8188, 'c': 0.2352, 'd': -0.008999, 'θ_start': 275, 'θ_end': 620},
            'Sagittarius-Carina': {'a': 4.2300, 'b': -1.1505, 'c': 0.1561, 'd': -0.005898, 'θ_start': 275, 'θ_end': 570},
            'Perseus': {'a': 0.9744, 'b': 0.1405, 'c': 0.003995, 'd': 0.0, 'θ_start': 280, 'θ_end': 500},
            'Local': {'a': 0.9887, 'b': 0.1714, 'c': 0.004358, 'd': 0.0, 'θ_start': 280, 'θ_end': 475},
            'Outer': {'a': 3.3846, 'b': -0.6554, 'c': 0.08170, 'd': 0.0, 'θ_start': 280, 'θ_end': 355}
        }

        return params

    
    def polynomial_log_spiral(self, θ, a, b, c, d):
        
        """Calculate radius using polynomial-logarithmic spiral equation.
        
        Parameters
        ----------
        θ : float or ndarray
            Galactic longitude angle in degrees
        a,b,c,d : float
            Polynomial coefficients from Hou & Han Table 4
            
        Returns
        -------
        float or ndarray
            Galactocentric radius in kiloparsecs
            
        Notes
        -----
        Implements equation:
        R(θ) = exp(a + bθ_rad + cθ_rad² + dθ_rad³)
        where θ_rad = np.radians(θ)
        """	
        return np.exp(a + b*np.radians(θ) + c*np.radians(θ)**2 + d*np.radians(θ)**3)
    
    def model_(self, arm_name, n_points=500):
        """Generate spiral arm coordinates in both coordinate systems."""
        
        params_ = self.getparams()
        params = params_[arm_name]
        
        
        θ = np.linspace(params['θ_start'], params['θ_end'], n_points)
        R = self.polynomial_log_spiral(θ, params['a'], params['b'], params['c'], params['d'])
        
        # Convert to Cartesian coordinates (Galactocentric)
        x_gc = R*np.cos(np.radians(θ))
        y_gc = R * np.sin(np.radians(θ))
        
        # Convert to Heliocentric coordinates
        x_hc = (x_gc + self.R0)

        return x_hc, y_gc, x_gc, y_gc
    
    
    
    def output_(self, arm, typ_='cartesian'):	
        
        """Get structured coordinate data for analysis/plotting."""

        xsun = self.xsun
        self.R0 = -xsun  # Solar Galactocentric radius (kpc)
    
        # Generate spiral arm coordinates
        xhc, yhc, xgc, ygc = self.model_(arm)
    
        if typ_ == 'cartesian':
            self.dout = {
                'xhc': xhc,
                'yhc': yhc,
                'xgc': xgc,
                'ygc': ygc
            }

    



class spiral_levine(object):
    
    """Levine et al. (2006) logarithmic spiral arm model for the Milky Way.
    
    Implements a four-arm logarithmic spiral model based on:
    Levine, E. S., Blitz, L., & Heiles, C. (2006). "The Spiral Structure 
    of the Outer Milky Way in Hydrogen". Astrophysical Journal.
    
    The model provides both galactocentric (GC) and heliocentric (HC) coordinates
    for each spiral arm segment with fixed pitch angles.

    Attributes
    ----------
    arms : numpy.ndarray
        Array of arm identifiers ['Arm1', 'Arm2', 'Arm3', 'Arm4']
    armcolour : dict
        Color mapping for visualization purposes:
        {'Arm1':'yellow', 'Arm2':'green', 'Arm3':'blue', 'Arm4':'purple'}
    arms_model : dict
        Dictionary containing spiral parameters for each arm:
        - pitch: Pitch angle in degrees
        - phi0: Solar crossing angle in degrees
    R0 : float
        Solar galactocentric radius in kpc (derived from xsun)

    Methods
    -------
    info()
        Display basic information about available arms
    model_(arm_name, R_max=25, n_points=1000)
        Generate coordinates for a specified arm
    plot_arms(coord_system='HC', R_max=25, show_sun=True)
        Visualize spiral arms in chosen coordinate system
    output_(arm, typ_='cartesian')
        Get structured coordinate data for analysis
    """
    
    
    def __init__(self):
        """Initialize spiral parameters from Levine et al. 2006"""
        
        self.getarmlist()
    
    def getarmlist(self):
        
        
        self.arms = np.array(['Arm1','Arm2','Arm3','Arm4'])
        self.armcolour = {'Arm1':'yellow','Arm2':'green','Arm3':'blue','Arm4':'purple'}
        self.getparams()

    
    def info(self):
        
        '''
      Displays basic informations about the models
        Prints a formatted table showing all arm identifiers to stdout.
        '''
    
        print('')
        print('------------------------')	
        dfmodlist = pd.DataFrame(self.arms,columns=['Arm list'])
        print(dfmodlist)
        print('------------------------')		
    
    
    def getparams(self):

        self.arms_model = {
            'Arm1': {'pitch': 24, 'phi0': 56},   # Pitch angle and Solar crossing angle
            'Arm2': {'pitch': 24, 'phi0': 135},
            'Arm3': {'pitch': 25, 'phi0': 189},
            'Arm4': {'pitch': 21, 'phi0': 234}
        }
            
        
    def model_(self,arm_name, R_max=25, n_points=1000):
        
        """Generate logarithmic spiral coordinates for specified arm.
        
        Parameters
        ----------
        arm_name : str
            Name of arm to model (must be in ['Arm1', 'Arm2', 'Arm3', 'Arm4'])
        R_max : float, optional
            Maximum galactocentric radius to model (kpc), default=25
        n_points : int, optional
            Number of points to sample along the spiral, default=1000

        Returns
        -------
        tuple
            (x_hc, y_hc, x_gc, y_gc) coordinate arrays where:
            - x_hc, y_hc: Heliocentric coordinates (kpc)
            - x_gc, y_gc: Galactocentric coordinates (kpc)

        Raises
        ------
        ValueError
            If invalid arm_name is provided

        Notes
        -----
        Implements the logarithmic spiral equation:
            R(φ) = R₀ * exp[(φ - φ₀) * tan(i)]
        where:
        - R₀ is solar galactocentric distance
        - i is pitch angle
        - φ₀ is solar crossing angle
        - φ is the angular coordinate
        """

        params = self.arms_model[arm_name]
        pitch_rad = np.radians(params['pitch'])
        phi0_rad = np.radians(params['phi0'])
        
        # Calculate maximum phi to reach R_max
        phi_max = phi0_rad + (np.log(R_max/self.R0)/np.tan(pitch_rad))
        
        # Generate angular range
        phi = np.linspace(phi0_rad, phi_max, n_points) #n_
        
        # Logarithmic spiral equation
        R = self.R0 * np.exp((phi - phi0_rad) * np.tan(pitch_rad))
        
        # Convert to Cartesian coordinates
        x_gc = R * np.cos(phi)
        y_gc = R * np.sin(phi)
        
        # Convert to Heliocentric coordinates
        x_hc = x_gc + self.R0  # Sun at (-R0, 0) in GC

        return x_hc, y_gc,x_gc, y_gc
    
    def plot_arms(self, coord_system='HC', R_max=25, show_sun=True):
        """Plot spiral arms in specified coordinate system"""
        plt.figure(figsize=(10, 10))
        colors = plt.cm.viridis(np.linspace(0, 1, len(self.arms)))
        
        for arm, color in zip(self.arms_model.keys(), colors):
            x_gc, y_gc, x_hc, y_hc = self.generate_arm(arm, R_max)
            
            if coord_system.upper() == 'GC':
                plt.plot(x_gc, y_gc, color=color, label=arm)
                plt.plot(-self.R0, 0, 'o', markersize=8, color='orange', label='Sun') if show_sun else None
                plt.xlabel('X (GC) [kpc]')
                plt.ylabel('Y (GC) [kpc]')
            elif coord_system.upper() == 'HC':
                plt.plot(x_hc, y_hc, color=color, label=arm)
                plt.plot(0, 0, 'o', markersize=8, color='orange', label='Sun') if show_sun else None
                plt.xlabel('X (HC) [kpc]')
                plt.ylabel('Y (HC) [kpc]')
            else:
                raise ValueError("Coordinate system must be 'GC' or 'HC'")
    
    def output_(self, arm, typ_='cartesian'):
        """Get structured coordinate data for analysis.
        
        Parameters
        ----------
        arm : str
            Name of arm to output (must be in self.arms)
        typ_ : {'cartesian'}, default 'cartesian'
            Output coordinate type (currently only cartesian supported)

        Returns
        -------
        dict
            Dictionary containing coordinate arrays:
            - 'xhc', 'yhc': Heliocentric coordinates (kpc)
            - 'xgc', 'ygc': Galactocentric coordinates (kpc)

        Notes
        -----
        Requires xsun attribute to be set for coordinate conversion
        """
    
        xsun = self.xsun
        self.R0 = -xsun  # Solar Galactocentric radius (kpc)
    
        xhc, yhc, xgc, ygc = self.model_(arm)
    
        if typ_ == 'cartesian':
            self.dout = {
                'xhc': xhc,
                'yhc': yhc,
                'xgc': xgc,
                'ygc': ygc
            }
    


class spiral_cepheids(object):
    '''
    
    June 28, 2024
    
    Usage: 
    spi = spiral_drimmel()
    spi.plot_(arm='1',color='b',typ_='HC')
    spi.plot_(arm='2',color='b',typ_='HC')
    spi.plot_(arm='all',color='b',typ_='HC')
    
    '''

    def __init__(self):

        self.loc = dataloc+'/DKPS_cepheids'
        self.fname = 'ArmAttributes_dyoungW1_bw025.pkl'
        self.getarmlist()
        
    def getarmlist(self):

        self.spirals = pickleread(self.loc+'/'+self.fname)
        self.arms= np.array(list(self.spirals['0']['arm_attributes'].keys()))

        self.armcolour = {'Scutum':'C3','Sag-Car':'C0','Orion':'C1','Perseus':'C2'}
    
    def info(self):
        
        '''
        here goes basic info for the user about this model
        '''

        print('')
        print('------------------------')	
        dfmodlist = pd.DataFrame(self.arms,columns=['Arm list'])
        print(dfmodlist)
        print('------------------------')		
        

    def output_(self,arm,typ_='cartesian'):		

        xsun = self.xsun
        rsun = -xsun	
        spirals = self.spirals
        arms = self.arms
        
                    
        # XY positions
        lnrsun = np.log(rsun) 
            
        # best phi range:
        phi_range = np.deg2rad(np.sort(self.spirals['1']['phi_range'].copy()))
        maxphi_range = np.deg2rad([60,-120]) 

        pang = (spirals['1']['arm_attributes'][arm]['arm_pang_strength']+spirals['1']['arm_attributes'][arm]['arm_pang_prom'])/2.
        lnr0 = (spirals['1']['arm_attributes'][arm]['arm_lgr0_strength']+spirals['1']['arm_attributes'][arm]['arm_lgr0_prom'])/2.
                        
        phi=(np.arange(51)/50.)*np.diff(phi_range)[0] + phi_range[0]  
        lgrarm = lnr0 - np.tan(np.deg2rad(pang))*phi 		
        
        xgc = -np.exp(lgrarm)*np.cos(phi); xhc = xgc - xsun
        ygc = np.exp(lgrarm)*np.sin(phi) ;  yhc = ygc
        
                        
        # extrapolate the arms
        phi=(np.arange(101)/100.)*np.diff(maxphi_range)[0] + maxphi_range[0]  
        lgrarm = lnr0 - np.tan(np.deg2rad(pang))*phi 
        
        xgc_ex = -np.exp(lgrarm)*np.cos(phi);  xhc_ex = xgc_ex - xsun
        ygc_ex = np.exp(lgrarm)*np.sin(phi); yhc_ex = ygc_ex
        lonarm = np.arctan((np.exp(lgrarm)*np.sin(phi))/(rsun - np.exp(lgrarm)*np.cos(phi))) 

        rgc = np.sqrt(xgc**2. + ygc**2.)
        rgc_ex = np.sqrt(xgc_ex**2. + ygc_ex**2.)

        if typ_ =='cartesian':
            
            # return xhc,yhc,xgc,ygc

            self.dout = {'xhc':xhc,
                         'yhc':yhc,
                         'xgc':xgc,
                         'ygc':ygc,	
                         'xhc_ex':xhc_ex,
                         'yhc_ex':yhc_ex,
                         'xgc_ex':xgc_ex,	
                         'ygc_ex':ygc_ex}	
            
        if typ_ =='polar':
                        
            
            phi1 = np.arctan2(yhc,-xgc)
            phi1_ex = np.arctan2(ygc_ex,-xgc_ex)
            
            phi2 = np.degrees(np.arctan(yhc/-xgc))
            phi3 = np.degrees(np.arctan2(yhc,xgc))%180.	
            phi4 = np.degrees(np.arctan2(yhc,xgc))%360.	
            
            plt.plot(phi1,rgc,'-',color=arm_clr[armi],markersize=markersize)
            plt.plot(phi1_ex,rgc_ex,linestyle=linestyle2,color=arm_clr[armi],markersize=markersize)
        
                        
            self.dused['rgc'].append(rgc)
            self.dused['xgc'].append(xgc)
            self.dused['yhc'].append(yhc)
            self.dused['phi1'].append(phi1)
            self.dused['phi4'].append(phi4)


        if typ_ =='polargrid':
            
            linewidth=2
            linestyle = '-'
            phi4 = np.degrees(np.arctan2(yhc,xgc))%360.	
            phi4_ex = np.degrees(np.arctan2(ygc_ex,xgc_ex))%360.	

            phi1 = np.arctan2(yhc,-xgc)
            phi1_ex = np.arctan2(ygc_ex,-xgc_ex)


            # plt.plot(np.radians(phi4),rgc,color=arm_clr[armi],markersize=markersize,linestyle=linestyle,linewidth=linewidth)

            # plt.plot(phi1,rgc,color=arm_clr[armi],markersize=markersize,linestyle=linestyle,linewidth=linewidth)
            # plt.plot(phi1_ex,rgc_ex,color=arm_clr[armi],markersize=markersize,linestyle='--',linewidth=linewidth)
            
            plt.plot(np.radians(phi4),rgc,color=arm_clr[armi],markersize=markersize,linestyle=linestyle,linewidth=linewidth)
            
            plt.plot(np.radians(phi4_ex),rgc_ex,color=arm_clr[armi],markersize=markersize,linestyle=linestyle2,linewidth=linewidth)
            # plt.plot(np.radians(phi4_ex),rgc_ex,color=arm_clr[armi],markersize=markersize,linestyle='--',linewidth=linewidth)


            self.dused['rgc'].append(rgc)
            self.dused['xgc'].append(xgc)
            self.dused['yhc'].append(yhc)
            self.dused['phi4'].append(phi4)
                
                    
        
    def plotit_(self,armplt='',typ_='GC',markersize=4,linewidth=2,linestyle2='--'):
        
        from time import sleep
        from scipy.signal import find_peaks
        import numpy as np
        import astropy
        import astropy.table as tb
        import pandas as pd
        import os
        import matplotlib as mpl
        import matplotlib.pyplot as plt
        import imp 
        import dtools
        import autil 
        import tabpy
        params = {'font.size':12,
              'text.usetex':False,
              'ytick.labelsize': 'medium',
              'legend.fontsize': 'large',
              'axes.linewidth': 1.0,
              'figure.dpi': 150.0,
              'xtick.labelsize': 'medium',
              'font.family': 'sans-serif',
              'axes.labelsize': 'medium'}
        mpl.rcParams.update(params)
        
        imp.reload(dtools)
        

        
        spirals = self.spirals
        
        # arms and plotting colors for the arms
        colors = ['C3','C0','C1','C2']
        arms = np.array(['Scutum','Sag-Car','Orion','Perseus'])
        
        figtyp = 'png'
        
        # XY positions
        rsun = self.rsun  # Might want to put these in a configuration file
        xsun = self.xsun  # Might want to put these in a configuration file
        lnrsun = np.log(rsun) 
        
        
        # best phi range:
        phi_range = np.deg2rad(np.sort(spirals['1']['phi_range'].copy()))
        maxphi_range = np.deg2rad([60,-120]) 
        
        
        # arms and plotting colors for the arms
        colors = ['C3','C0','C1','C2']
        arms = np.array(self.armlist)
        
        arm_clr = {'Scutum':'C3','Sag-Car':'C0','Orion':'C1','Perseus':'C2'}
        self.arm_clr = arm_clr
        
        dt = {}
        
        
        for armi in np.arange(arms.size):
            
            arm = arms[armi]
            pang = (spirals['1']['arm_attributes'][arm]['arm_pang_strength']+spirals['1']['arm_attributes'][arm]['arm_pang_prom'])/2.
            lnr0 = (spirals['1']['arm_attributes'][arm]['arm_lgr0_strength']+spirals['1']['arm_attributes'][arm]['arm_lgr0_prom'])/2.
            
                        
            
            # plot the arms
            
            
            phi=(np.arange(51)/50.)*np.diff(phi_range)[0] + phi_range[0]  
            lgrarm = lnr0 - np.tan(np.deg2rad(pang))*phi 
            
            
            xgc = -np.exp(lgrarm)*np.cos(phi); xhc = xgc - xsun
            ygc = np.exp(lgrarm)*np.sin(phi) ;  yhc = ygc
            
                            
            # extrapolate the arms
            phi=(np.arange(101)/100.)*np.diff(maxphi_range)[0] + maxphi_range[0]  
            lgrarm = lnr0 - np.tan(np.deg2rad(pang))*phi 
            
            xgc_ex = -np.exp(lgrarm)*np.cos(phi);  xhc_ex = xgc_ex - xsun
            ygc_ex = np.exp(lgrarm)*np.sin(phi); yhc_ex = ygc_ex
            lonarm = np.arctan((np.exp(lgrarm)*np.sin(phi))/(rsun - np.exp(lgrarm)*np.cos(phi))) 
            
            dt[arm] = {}
            dt[arm]['xgc'] = xgc
            dt[arm]['xhc'] = xhc
            dt[arm]['ygc'] = ygc
            dt[arm]['yhc'] = yhc
                        
            dt[arm]['xgc_ex'] = xgc_ex
            dt[arm]['xhc_ex'] = xhc_ex
            dt[arm]['ygc_ex'] = ygc_ex
            dt[arm]['yhc_ex'] = yhc_ex
                        


        self.dused = {}
        self.dused['rgc'] = []
        self.dused['xgc'] = []
        self.dused['yhc'] = []
        self.dused['phi1'] = []
        self.dused['phi4'] = []
        


        # for armi in dt.keys():
        for armi in armplt:
            # print(armplt)
                        
            xgc = dt[armi]['xgc']
            ygc = dt[armi]['ygc']
            xhc = dt[armi]['xhc']
            yhc = dt[armi]['yhc']
            
            xgc_ex = dt[armi]['xgc_ex']
            ygc_ex = dt[armi]['ygc_ex']
            xhc_ex = dt[armi]['xhc_ex']
            yhc_ex = dt[armi]['yhc_ex']			


            rgc = np.sqrt(xgc**2. + ygc**2.)
            rgc_ex = np.sqrt(xgc_ex**2. + ygc_ex**2.)



            if typ_ == 'GC':
                

                
                plt.plot(xgc,ygc,'-',color=arm_clr[armi])				
                plt.plot(xgc_ex,ygc_ex,linestyle=linestyle2,color=arm_clr[armi])
                
                plt.axvline(xsun,linewidth=1,linestyle='--')			
                plt.axhline(0,linewidth=1,linestyle='--')			
                
    
                plt.plot(0.,0.,marker='+',markersize=10,color='black')
                plt.plot(xsun,0.,marker='o',markersize=10,color='black')				
    
                plt.xlabel('X$_{GC}$')
                plt.ylabel('Y$_{GC}$')
                    
                
                
                
                # # labels
                # plt.text(-2,-5,'Scutum',fontsize=14,fontweight='bold',color=colors[0])
                # plt.text(-2,-10,'Sgr-Car',fontsize=14,fontweight='bold',color=colors[1])
                # plt.text(-3,-13,'Local',fontsize=14,fontweight='bold',color=colors[2])
                # plt.text(-9,-14,'Perseus',fontsize=14,fontweight='bold',color=colors[3])		
        
        
            if typ_ == 'HC':	
                
                
        
            
                
                # plt.plot(xhc,yhc,color,label=arm,linestyle=linestyle,linewidth=linewidth,markersize=2)
                # plt.plot(xhc,yhc,color,linestyle=linestyle,linewidth=linewidth,markersize=2)
                
                
                plt.plot(xhc,yhc,'-',color=arm_clr[armi])				
                plt.plot(xhc_ex,yhc_ex,linestyle=linestyle2,color=arm_clr[armi])
    
                plt.plot(0.,0.,marker='o',markersize=markersize,color='black')
                plt.plot(-xsun,0.,marker='+',markersize=markersize,color='black')						
                                
    
                
                plt.xlabel('X$_{HC}$')
                plt.ylabel('Y$_{HC}$')			
    
    
    
    
            if typ_ =='polar':
                            
                
                phi1 = np.arctan2(yhc,-xgc)
                phi1_ex = np.arctan2(ygc_ex,-xgc_ex)
                
                phi2 = np.degrees(np.arctan(yhc/-xgc))
                phi3 = np.degrees(np.arctan2(yhc,xgc))%180.	
                phi4 = np.degrees(np.arctan2(yhc,xgc))%360.	
                
                plt.plot(phi1,rgc,'-',color=arm_clr[armi],markersize=markersize)
                plt.plot(phi1_ex,rgc_ex,linestyle=linestyle2,color=arm_clr[armi],markersize=markersize)
            
                            
                self.dused['rgc'].append(rgc)
                self.dused['xgc'].append(xgc)
                self.dused['yhc'].append(yhc)
                self.dused['phi1'].append(phi1)
                self.dused['phi4'].append(phi4)


            if typ_ =='polargrid':
                
                linewidth=2
                linestyle = '-'
                phi4 = np.degrees(np.arctan2(yhc,xgc))%360.	
                phi4_ex = np.degrees(np.arctan2(ygc_ex,xgc_ex))%360.	

                phi1 = np.arctan2(yhc,-xgc)
                phi1_ex = np.arctan2(ygc_ex,-xgc_ex)
    

                # plt.plot(np.radians(phi4),rgc,color=arm_clr[armi],markersize=markersize,linestyle=linestyle,linewidth=linewidth)

                # plt.plot(phi1,rgc,color=arm_clr[armi],markersize=markersize,linestyle=linestyle,linewidth=linewidth)
                # plt.plot(phi1_ex,rgc_ex,color=arm_clr[armi],markersize=markersize,linestyle='--',linewidth=linewidth)
                
                plt.plot(np.radians(phi4),rgc,color=arm_clr[armi],markersize=markersize,linestyle=linestyle,linewidth=linewidth)
                
                plt.plot(np.radians(phi4_ex),rgc_ex,color=arm_clr[armi],markersize=markersize,linestyle=linestyle2,linewidth=linewidth)
                # plt.plot(np.radians(phi4_ex),rgc_ex,color=arm_clr[armi],markersize=markersize,linestyle='--',linewidth=linewidth)

    
                self.dused['rgc'].append(rgc)
                self.dused['xgc'].append(xgc)
                self.dused['yhc'].append(yhc)
                self.dused['phi4'].append(phi4)
                
class spiral_drimmel(object):

    """Drimmel (2000) Near-Infrared (NIR) spiral arm model
    
    Implements the 2-arm spiral structure model from:
    Drimmel, R. (2000) "Evidence for a two-armed spiral in the Milky Way"
    using COBE/DIRBE near-infrared data. Includes main arms and phase-shifted interarms.

    Attributes
    ----------
    arms : ndarray
        Array of arm identifiers ['1_arm', '2_arm', '3_interarm', '4_interarm']
    armcolour : dict
        Color mapping for visualization:
        - Main arms: black
        - Interarms: red
    data : dict
        Dictionary containing arm coordinates and parameters

    Methods
    -------
    info()
        Display available arm components
    getdata()
        Load and preprocess spiral arm data
    output_(arm, typ_)
        Retrieve coordinate data in specified format
    """


    def __init__(self):
        """Initialize Drimmel NIR spiral model with default parameters"""
     
        self.loc = dataloc+'/Drimmel_NIR'
        self.fname = 'Drimmel2armspiral.fits'
        self.getarmlist()
        
    def getarmlist(self):
        """Initialize arm identifiers and visualization scheme.
        
        Sets:
        - arms: Array of 4 components (2 main arms + 2 interarms)
        - armcolour: Color mapping dictionary
        """
        self.arms = np.array(['1_arm','2_arm','3_interarm','4_interarm'])
        self.armcolour = {'1_arm':'black','2_arm':'black','3_interarm':'red','4_interarm':'red'}
    
    def info(self):
        
        """Display basic model information and arm components.
        
        Prints formatted table of arm identifiers to stdout.
        """

        print('')
        print('------------------------')	
        dfmodlist = pd.DataFrame(self.arms,columns=['Arm list'])
        print(dfmodlist)
        print('------------------------')		
        
    
    def getdata(self):
        """Load and preprocess spiral arm data from FITS file.
        
        Performs:
        1. Loads base FITS data
        2. Scales coordinates using solar position
        3. Adds phase-shifted interarm components
        4. Calculates galactocentric radii
        
        Notes
        -----
        - Original data scaled by solar galactocentric distance
        - Phase-shifted arms loaded from separate numpy files
        - Calculates R_GC = sqrt((x + X_sun)^2 + y^2)
        """

        dt = fitsread(self.loc+'/'+self.fname)
        self.data0 = dt.copy()
        
        xsun = self.xsun						
            
        # rescaling to |xsun|
        qnts = ['rgc1','xhc1','yhc1','rgc2','xhc2','yhc2']
        for qnt in qnts:
            dt[qnt] = dt[qnt]*abs(xsun)				
        
        
        #----- add phase-shifted arms as `3` and `4`
        
    
    
        dloc = self.loc+'/phase_shifted'
        for inum in [3,4]:
            dt['xhc'+str(inum)] = np.load(dloc+'/Arm'+str(inum)+'_X_hel.npy')
            dt['yhc'+str(inum)] = np.load(dloc+'/Arm'+str(inum)+'_Y_hel.npy')
            dt['rgc'+str(inum)] = np.sqrt( ((dt['xhc'+str(inum)] + xsun)**2.) + ((dt['yhc'+str(inum)])**2.) )
        
        
        #------------------
        
        
        
        self.data = dt.copy()

        return 


    def output_(self,arm,typ_='cartesian'):			
        """Retrieve spiral arm coordinates in specified format.
        
        Parameters
        ----------
        arm : str
            Arm identifier or selection mode:
            - '1', '2' for main arms
            - '3', '4' for interarms 
            - 'all' for all components
            - 'main' for just main arms
        typ_ : {'cartesian', 'polar', 'polargrid'}, default 'cartesian'
            Output format:
            - cartesian: Returns x,y coordinates
            - polar/polargrid: Generates polar coordinate plots

        Returns
        -------
        dict
            For cartesian type contains:
            - xhc, yhc: Heliocentric coordinates (kpc)
            - xgc, ygc: Galactocentric coordinates (kpc)
            
        Notes
        -----
        Polar modes create matplotlib plots directly using:
        - phi1: Angle from negative x-axis (GC frame)
        - phi4: Galactic longitude (0-360 degrees)
        """
        xsun = self.xsun
        self.getdata()
        dt = self.data.copy()
        
    
                    
        numbs = [arm]
        if arm == 'all':
            numbs = self.arms
        elif arm == 'main':
            numbs = ['1','2']		
        
        self.dused = {}
        self.dused['rgc'] = []
        self.dused['xgc'] = []
        self.dused['yhc'] = []
        self.dused['phi1'] = []
        self.dused['phi4'] = []

        for numb1 in numbs:	
            numb = str(int(numb1.split('_')[0]))	
            
            xhc = dt['xhc'+numb]
            yhc = dt['yhc'+numb]
            rgc = dt['rgc'+numb]
            
            xgc = xhc + xsun			
            ygc = yhc
        
            if typ_ == 'cartesian':
                
                self.dout = {'xhc':xhc,
                             'yhc':yhc,
                             'xgc':xgc,
                             'ygc':ygc}					
                
            

            if typ_ =='polar':
                

                phi1 = np.arctan2(yhc,-xgc)
                
                phi2 = np.degrees(np.arctan(yhc/-xgc))
                phi3 = np.degrees(np.arctan2(yhc,xgc))%180.	
                phi4 = np.degrees(np.arctan2(yhc,xgc))%360.	
                
                # phi3 = 180.-np.degrees(phi1)
                
                # phi1 = (np.arctan2(yhc,xgc))	
                # plt.plot(np.degrees(phi1),rgc,color,linestyle='--',linewidth=linewidth)
                # plt.plot(np.degrees(phi1),rgc,'.',color='blue')
                plt.plot(phi1,rgc,color=color,markersize=markersize,linestyle=linestyle,linewidth=linewidth)

                self.dused['rgc'].append(rgc)
                self.dused['xgc'].append(xgc)
                self.dused['yhc'].append(yhc)
                self.dused['phi1'].append(phi1)
                self.dused['phi4'].append(phi4)
                
                
            if typ_ =='polargrid':
                

                phi1 = np.arctan2(yhc,-xgc)
                
                phi2 = np.degrees(np.arctan(yhc/-xgc))
                phi3 = np.degrees(np.arctan2(yhc,xgc))%180.	
                phi4 = np.degrees(np.arctan2(yhc,xgc))%360.	
                
                # phi3 = 180.-np.degrees(phi1)


                if numb == numbs[0]:
                    plt.plot(np.radians(phi4),rgc,color=color,markersize=markersize,linestyle=linestyle,linewidth=linewidth,label='NIR')

                else:
                    plt.plot(np.radians(phi4),rgc,color=color,markersize=markersize,linestyle=linestyle,linewidth=linewidth)
                    



                self.dused['rgc'].append(rgc)
                self.dused['xgc'].append(xgc)
                self.dused['yhc'].append(yhc)
                self.dused['phi1'].append(phi1)
                self.dused['phi4'].append(phi4)
                
                
                # plt.plot(xgc,yhc,'.',color=color)
        
                # plt.legend() 
                return 



class reid_spiral(object):
	"""Reid et al. (2019) kinked logarithmic spiral arm model
	
	Implements the Milky Way spiral structure model from:
	"Trigonometric Parallaxes of High Mass Star Forming Regions: The Structure and Kinematics of the Milky Way"
	using kinked logarithmic spirals with varying pitch angles. Models 7 major arm features.
	
	Attributes
	----------
	arms : ndarray
		Array of arm identifiers ['3-kpc', 'Norma', 'Sct-Cen', 'Sgr-Car', 'Local', 'Perseus', 'Outer']
	armcolour : dict
		Color mapping for visualization purposes
	kcor : bool
		Flag for kinematic distance correction adjustment
	params : dict
		Dictionary containing spiral parameters for each arm
	
	Methods
	-------
	info()
		Display basic information about available arms
	model_(params)
		Generate spiral coordinates with kink parameters
	output_(arm, typ_)
		Get structured coordinate data
	"""
	
	def __init__(self, kcor=False):
		"""Initialize Reid et al. (2019) spiral model
		
		Parameters
		----------
		kcor : bool, optional
			Apply kinematic distance correction adjustment to R_kink parameters,
			default=False
		"""
		self.kcor = kcor
		self.getarmlist()
	
	
	def getarmlist(self):
		
		# self.arms = np.array(['3-kpc','Norma','Sct-Cen','Sgt-Car','Local','Perseus','Outer'])
		self.arms = np.array(['3-kpc','Norma','Sct-Cen','Sgr-Car','Local','Perseus','Outer'])      
		
		
		self.armcolour = {'3-kpc':'C6','Norma':'C5','Sct-Cen':'C4','Sgr-Car':'C3','Local':'C2','Perseus':'C1','Outer':'C0'}		  
		
	def info(self):
		
		'''
		here goes basic info for the user about this model
		'''
	
		print('')
		print('------------------------')	
		dfmodlist = pd.DataFrame(self.arms,columns=['Arm list'])
		print(dfmodlist)
		print('------------------------')		
		
		
	def getparams(self,arm):
		"""Load spiral parameters for specified arm from Reid et al. (2019) Table 4.
		
		Parameters
		----------
		arm : str
			Valid arm identifier from class arms list
	
		Returns
		-------
		dict
			Dictionary containing:
			- beta_kink: Kink angle position in degrees
			- pitch_low: Pitch angle before kink (degrees)
			- pitch_high: Pitch angle after kink (degrees)
			- R_kink: Galactocentric radius at kink (kpc)
			- beta_min/max: Angular range in degrees
			- width: Arm width parameter (kpc)
	
		Notes
		-----
		Applies kinematic correction to R_kink if kcor=True during initialization
		"""
		if arm == '3-kpc':
			params = {'name':arm,'beta_kink':15,'pitch_low':-4.2,'pitch_high':-4.2,'R_kink':3.52,'beta_min':15,'beta_max':18,'width':0.18}
		if arm == 'Norma':
			params = {'name':arm,'beta_kink':18,'pitch_low':-1.,'pitch_high':19.5,'R_kink':4.46,'beta_min':5,'beta_max':54,'width':0.14}
		if arm == 'Sct-Cen':
			params = {'name':arm,'beta_kink':23,'pitch_low':14.1,'pitch_high':12.1,'R_kink':4.91,'beta_min':0,'beta_max':104,'width':0.23}
		if arm == 'Sgr-Car': #'Sgr-Car'
			params = {'name':arm,'beta_kink':24,'pitch_low':17.1,'pitch_high':1,'R_kink':6.04,'beta_min':2,'beta_max':97,'width':0.27}
		if arm == 'Local':
			params = {'name':arm,'beta_kink':9,'pitch_low':11.4,'pitch_high':11.4,'R_kink':8.26,'beta_min':-8,'beta_max':34,'width':0.31}
		if arm == 'Perseus':
			params = {'name':arm,'beta_kink':40,'pitch_low':10.3,'pitch_high':8.7,'R_kink':8.87,'beta_min':-23,'beta_max':115,'width':0.35}
		if arm == 'Outer':
			params = {'name':arm,'beta_kink':18,'pitch_low':3,'pitch_high':9.4,'R_kink':12.24,'beta_min':-16,'beta_max':71,'width':0.65}
		
		
		if self.kcor:
			Rreid = 8.15
			diffval = params['R_kink'] - Rreid
			xsun = get_lsr()['xsun']
			if diffval < 0:
				 params['R_kink'] = (-xsun) + diffval
			else:
				 params['R_kink'] = (-xsun) + diffval
					
		
		return params
	
	def model_(self,params):
		"""Generate kinked logarithmic spiral coordinates.
		
		Parameters
		----------
		params : dict
			Spiral parameters dictionary from getparams()
	
		Returns
		-------
		tuple
			(x, y, x1, y1, x2, y2) coordinate arrays where:
			- x,y: Arm center coordinates (GC)
			- x1,y1: Inner arm boundary
			- x2,y2: Outer arm boundary
	
		Notes
		-----
		Implements modified logarithmic spiral equation with pitch angle kink:
		R(β) = R_kink * exp[-(β - β_kink) * tan(pitch)]
		where pitch changes at β_kink
		"""
		
		beta_kink = np.radians(params['beta_kink'])
		pitch_low = np.radians(params['pitch_low'])
		pitch_high = np.radians(params['pitch_high'])
		R_kink = params['R_kink']
		beta_min = params['beta_min']
		beta_max = params['beta_max']
		width = params['width']
		
		
		# beta = np.linspace(beta_min-180,beta_max,100)
		beta = np.linspace(beta_min,beta_max,1000)
	
	
		beta_min = np.radians(beta_min)
		beta_max = np.radians(beta_max)
		beta = np.radians(beta)	
		
		
		pitch = np.zeros(beta.size) + np.nan
		indl = np.where(beta<beta_kink)[0]; pitch[indl] = pitch_low
		indr = np.where(beta>beta_kink)[0]; pitch[indr] = pitch_high
		
		tmp1 = (beta - beta_kink)*(np.tan(pitch))
		tmp2 = np.exp(-tmp1)
				
		R = R_kink*tmp2
		x = -R*(np.cos(beta))
		y = R*(np.sin(beta))
	
		##3 testing 
		R2 = (R_kink+(width*0.5))*tmp2
		x2 = -R2*(np.cos(beta))
		y2 = R2*(np.sin(beta))
	
		R1 = (R_kink-(width*0.5))*tmp2
		x1 = -R1*(np.cos(beta))
		y1 = R1*(np.sin(beta))
		
		
		
		return x,y, x1,y1,x2,y2
	
	def output_(self,arm,typ_='cartesian'):	
		"""Get structured coordinate data for analysis/plotting.
		Returns
		-------
		dict
			For 'cartesian' type contains:
			- xhc, yhc: Heliocentric coordinates (kpc)
			- xgc, ygc: Galactocentric coordinates (kpc)
	
		Notes
		-----
		Polar modes create matplotlib plots directly
		"""
		xsun = self.xsun
		params = self.getparams(arm)
		
		if typ_ =='cartesian':
	
			xgc,ygc,xgc1,ygc1,xgc2,ygc2 = self.model_(params);			
			xhc = xgc - xsun
			xhc1 = xgc1 - xsun
			xhc2 = xgc2 - xsun
	
			yhc = ygc
			
			self.dout = {'xhc':xhc,
						 'yhc':yhc,
						 'xgc':xgc,
						 'ygc':ygc}								
			
		
		if typ_ =='polar':
			
			xhc = x - xsun
			xhc1 = x1 - xsun
			xhc2 = x2 - xsun
			
			rgc = sqrtsum(ds=[x,y])
			phi1 = np.arctan2(y,-x)
			phi2 = np.degrees(np.arctan(y/-x))
			phi3 = np.degrees(np.arctan2(y,x))%180.	
			
			# phi3 = 180.-np.degrees(phi1)
			
			# phi1 = (np.arctan2(yhc,xgc))	
			# plt.plot(phi1,rgc,color,linestyle='-',linewidth=linewidth)
			plt.plot(phi1,rgc,'.',color=color,markersize=markersize)
			
			return 
			
		if typ_ =='polargrid':
			
			linewidth=2
			
			yhc = y
			xgc = x
			phi4 = np.degrees(np.arctan2(yhc,xgc))%360.	
			rgc = sqrtsum(ds=[x,y])
	
			plt.plot(np.radians(phi4),rgc,color=color,markersize=markersize,linestyle=linestyle,linewidth=linewidth,label=arm)
	
	
	
			
			return 
	



#-------------------------
# main class:
#-------------------------

class main_(object):
    
    def __init__(self,xsun=-8.277):
        

        self.root_ = root_
        self.dataloc = dataloc
        
        self.xsun = xsun
        self.Rsun = -self.xsun
        
        self.listmodels()
        self.getinfo()	
    
    def listmodels(self):
        
        '''
        think of a name check exception
        '''
        
        self.models = ['Taylor_Cordes_1992','Drimmel_NIR_2000','Levine_2006','Hou_Han_2014','Reid_2019','Poggio_2021','Drimmel_ceph_2024']
        # self.models = ['Drimmel_NIR_2000','Levine_2006','Hou_Han_2014','Reid_2019','Poggio_2021']
        
        self.models_class = {'Reid_2019':reid_spiral(),
                             'Levine_2006':spiral_levine(),
                             'Poggio_2021':spiral_eloisa(),
                             'Drimmel_NIR_2000':spiral_drimmel(),
                             'Taylor_Cordes_1992':TaylorCordesSpiral(),
                             'Hou_Han_2014':spiral_houhan(),
                             'Drimmel_ceph_2024':spiral_cepheids()}
    

    def getinfo(self,model=''):

        '''
        
        
        plotattrs_description:
        
        
        'plot': 
        setting this True/False allows plotting or not
                
        'markersize':
        used for some models 
        
        'coordsys':
        'HC' (heliocentric) or 'GC' (galactocentric)
        'linewidth':0.8,
        'linestyle': '-',
        'armcolour':'',
        'markSunGC':True,
        'xmin':'',
        'xmax':'',
        'ymin':'',
        'ymax':'',
        'polargrid':False}		

        '''

        if model == '':

            print('try self.getinfo(model) for more details')
            print('')
            print('------------------------')
            # print('List of available models:')
            dfmodlist = pd.DataFrame(self.models,columns=['Available models:'])
            print(dfmodlist)
            print('------------------------')
        else:
            spimod = self.models_class[model]
            print('#####################')			
            print('Model = '+model)
            spimod.info()
            
            
        self.plotattrs_default = {'plot':False,
                                'markersize':3,
                                'coordsys':'HC',
                                'linewidth':0.8,
                                'linestyle': '-',
                                'armcolour':'',
                                'markSunGC':True,
                                'xmin':'',
                                'xmax':'',
                                'ymin':'',
                                'ymax':'',
                                'polargrid':False}
        
    
        
    
    def add2plot(self,plotattrs):
        
        if plotattrs['coordsys'] =='HC':					
            # hc case					

            plt.axvline(0,linewidth=1,linestyle='--')			
            plt.axhline(0,linewidth=1,linestyle='--')		
            plt.plot(0.,0.,marker=r'$\odot$',markersize=plotattrs['markersize'],color='black')
            plt.plot(-self.xsun,0.,marker='*',markersize=plotattrs['markersize'],color='black')	


        if plotattrs['coordsys'] =='GC':							
            # gc case				
            
            plt.axvline(self.xsun,linewidth=1,linestyle='--')			
            plt.axhline(0,linewidth=1,linestyle='--')			
            plt.plot(0.,0.,marker='*',markersize=plotattrs['markersize'],color='black')
            plt.plot(self.xsun,0.,marker=r'$\odot$',markersize=plotattrs['markersize'],color='black')
            

    def readout(self,plotattrs={},model='',arm='',print_=False):
        '''
        


        # def plot_(self,arm,color='',typ_='HC',xsun_=[]		
        '''

        
        
        if model == '':
             raise RuntimeError('model = blank | no model provided \n try self.getino() for list of available models')
             

        spimod = self.models_class[model]			
        spimod.xsun = self.xsun
        spimod.getarmlist()	

        self.armlist = spimod.arms

        if 'poggio' in model.lower():		
            spimod.output_(coordsys=plotattrs['coordsys'])	

        else:

            # in case plot attributes are not provided, or incomplete
            for ky in self.plotattrs_default.keys():			
                if ky not in list(plotattrs.keys()):				
                    plotattrs[ky] = self.plotattrs_default[ky]
    
            if arm != 'all':		
    
                spimod.output_(arm)
                                                
                spimod.dout['rgc'] = sqrtsum(ds=[spimod.dout['xgc'],spimod.dout['ygc']])						
                spimod.dout['phi1'] = np.arctan2(spimod.dout['yhc'],-spimod.dout['xgc']);  self.dout = spimod.dout.copy() 


                                # plt.plot(phi1,rgc,'-',color=arm_clr[armi],markersize=markersize)					
    
        
                if plotattrs['plot']:				
    
                    if plotattrs['armcolour'] == '':
                        plotattrs['armcolour'] = spimod.armcolour[arm]				
                    plt.plot(spimod.dout['x'+plotattrs['coordsys'].lower()],spimod.dout['y'+plotattrs['coordsys'].lower()],'.',color=plotattrs['armcolour'])	
                    
                    if 'xhc_ex' in 	spimod.dout.keys():
                        plt.plot(spimod.dout['x'+plotattrs['coordsys'].lower()+'_ex'],spimod.dout['y'+plotattrs['coordsys'].lower()+'_ex'],'--',color=plotattrs['armcolour'])						
                    
    
                    
    
                    plt.xlabel('X$_{'+plotattrs['coordsys']+'}$ [Kpc]')
                    plt.ylabel('Y$_{'+plotattrs['coordsys']+'}$ [Kpc]')

                    if plotattrs['xmin'] == '' or plotattrs['xmax'] == '' or plotattrs['ymin'] == '' or plotattrs['ymax'] == '' :						
                        1+1
                                                                            
                    else:
                        xmin,xmax = plotattrs['xmin'],plotattrs['xmax']
                        ymin,ymax = plotattrs['ymin'],plotattrs['ymax']
    
                        plt.xlim([xmin,xmax])	
                        plt.ylim([ymin,ymax])	
                                        
                    

                
                    self.xmin,self.xmax =plt.gca().get_xlim()[0],plt.gca().get_xlim()[1]				
                    self.ymin,self.ymax =plt.gca().get_ylim()[0],plt.gca().get_ylim()[1]	
                    if plotattrs['polargrid']:
                        add_polargrid(xmin=self.xmin,xmax=self.xmax,ymin=self.ymin,ymax=self.ymax)
				                   

                        
            elif arm =='all':
    
                for arm_temp in spimod.arms:
                    spimod.output_(arm_temp)
                    
                    if plotattrs['plot']:
                        
                        plt.plot(spimod.dout['x'+plotattrs['coordsys'].lower()],spimod.dout['y'+plotattrs['coordsys'].lower()],'.',color=spimod.armcolour[arm_temp])
    
                        if 'xhc_ex' in 	spimod.dout.keys():
                            plt.plot(spimod.dout['x'+plotattrs['coordsys'].lower()+'_ex'],spimod.dout['y'+plotattrs['coordsys'].lower()+'_ex'],'--',color=spimod.armcolour[arm_temp])						
        
        
    
                        plt.xlabel('X$_{'+plotattrs['coordsys']+'}$ [Kpc]')
                        plt.ylabel('Y$_{'+plotattrs['coordsys']+'}$ [Kpc]')
                        
        
                        if plotattrs['xmin'] == '' or plotattrs['xmax'] == '' or plotattrs['ymin'] == '' or plotattrs['ymax'] == '' :
                            1+1
                            
    
                                        
                        else:
                            xmin,xmax = plotattrs['xmin'],plotattrs['xmax']
                            ymin,ymax = plotattrs['ymin'],plotattrs['ymax']
    
                            # xmin,xmax = np.nanmin(spimod.dout['x'+plotattrs['coordsys'].lower()]) -3,np.nanmax(spimod.dout['x'+plotattrs['coordsys'].lower()]) + 3
                            # ymin,ymax = np.nanmin(spimod.dout['y'+plotattrs['coordsys'].lower()]) -3 ,np.nanmax(spimod.dout['y'+plotattrs['coordsys'].lower()]) + 3
        
                            plt.xlim([xmin,xmax])	
                            plt.ylim([ymin,ymax])	
                    
                    
                    
                        self.xmin,self.xmax =plt.gca().get_xlim()[0],plt.gca().get_xlim()[1]				
                        self.ymin,self.ymax =plt.gca().get_ylim()[0],plt.gca().get_ylim()[1]	
                        
                        if plotattrs['markSunGC']:
                            self.add2plot(plotattrs)
                    self.dout = spimod.dout.copy()
                    
    


                                  
            

            
            if plotattrs['polargrid']:
                add_polargrid(xmin=self.xmin,xmax=self.xmax,ymin=self.ymin,ymax=self.ymax)			
            self.plotattrs = plotattrs				

        return 










