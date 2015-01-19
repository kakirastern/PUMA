import atpy
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc
#import matplotlib.gridspec as gridspec
#from matplotlib.patches import Ellipse
#import statsmodels.api as sm
import optparse
from astroML.plotting import hist

parser = optparse.OptionParser()

parser.add_option('-v', '--input_vot', 
	help='Enter name of input .vot table')

options, args = parser.parse_args()

input_vot = options.input_vot


class source_info:
	def __init__(self):
		self.name = None
		self.ra = None
		self.dec = None
		self.rerr = None
		self.derr = None
		self.SI = None
		self.intercept = None
		self.SI_err = None
		self.intercept_err = None
		self.num_match = None
		self.retained_match = None
		self.type_match = None
		self.low_resid = None
		self.f180 = None
		self.f180_ext = None
		self.num_cats = None

tdata = atpy.Table(input_vot,verbose=False)


names = tdata['mwacs_name']
ras = tdata['updated_RA_J2000']
decs = tdata['updated_DEC_J2000']
rerrs = tdata['updated_RA_err']
derrs = tdata['updated_DEC_err']
SIs = tdata['SI']
intercepts = tdata['Intercept']
SI_errs = tdata['e_SI']
intercept_errs = tdata['e_Intercept']
num_cats = tdata['Number_cats']
num_matches = tdata['Number_matches']
retained_matches = tdata['Retained_matches']
type_matches = tdata['Type_matches']
low_resids = tdata['Low_resids']
f180s = tdata['S_180']
f180_exts = tdata['S_180.0_ext']

def make_source(ind):
	source=source_info()
	source.name = names[ind]
	source.ra = ras[ind]
	source.dec = decs[ind]
	source.rerr = rerrs[ind]
	source.derr = derrs[ind]
	source.SI = SIs[ind]
	source.intercept = intercepts[ind]
	source.SI_err = SI_errs[ind] 
	source.intercept_err = intercept_errs[ind]
	source.num_match = num_matches[ind]
	source.retained_match = retained_matches[ind]
	source.type_match = type_matches[ind]
	source.low_resid = low_resids[ind]
	source.f180 = f180s[ind]
	source.f180_ext = f180_exts[ind]
	source.num_cats = num_cats[ind]
	return source

##Populate all the sources
sources = []
for i in xrange(len(names)): sources.append(make_source(i))

##Plot the SI dist of good vs bad fits-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

from matplotlib import rc

font = {'size': 14}
rc('font', **font)

fig_hist = plt.figure(figsize=(15,10))

##-----------------------------------------------------------------------------------------------------------------------
ax1 = fig_hist.add_subplot(221)
##Plot the histograms using bayesian blocks 
hist(SIs,bins='blocks',ax=ax1,histtype='step',normed=True,color='k',linewidth=3.0,label='All fits (%d sources)' %len(SIs))

##-----------------------------------------------------------------------------------------------------------------------
ax2 = fig_hist.add_subplot(222)
good_fit_SIs = [source.SI for source in sources if source.low_resid==0]
bad_fit_SIs = [source.SI for source in sources if source.low_resid==1]
hist(good_fit_SIs,bins='blocks',ax=ax2,histtype='step',normed=True,color='k',linewidth=3.0,label='Good fits \n(%d sources)' %len(good_fit_SIs))
hist(bad_fit_SIs,bins='blocks',ax=ax2,histtype='step',normed=True,color='r',linewidth=3.0,label='Bad fits \n(%d sources)' %len(bad_fit_SIs))

##-----------------------------------------------------------------------------------------------------------------------
ax3 = fig_hist.add_subplot(223)
two_cat_SIs = [source.SI for source in sources if source.num_cats==2]
nottwo_cat_SIs = [source.SI for source in sources if source.num_cats!=2]
hist(two_cat_SIs,bins='blocks',ax=ax3,histtype='step',normed=True,color='r',linewidth=3.0,label='More than two \ncatalogues \n(%d sources)' %len(two_cat_SIs))
hist(nottwo_cat_SIs,bins='blocks',ax=ax3,histtype='step',normed=True,color='k',linewidth=3.0,label='Only two \ncatalogues \n(%d sources)' %len(nottwo_cat_SIs))

##-----------------------------------------------------------------------------------------------------------------------
ax4 = fig_hist.add_subplot(224)
pos_match = [source.SI for source in sources if source.type_match=='position']
spec_match = [source.SI for source in sources if source.type_match=='spectral']
comb_match = [source.SI for source in sources if source.type_match=='combine']

hist(pos_match,bins='blocks',ax=ax4,histtype='step',normed=True,color='k',linewidth=3.0,label='Positional match \n(%d sources)' %len(pos_match))
hist(spec_match,bins='blocks',ax=ax4,histtype='step',normed=True,color='c',linewidth=3.0,label='Spectral match \n(%d sources)' %len(spec_match))
hist(comb_match,bins='blocks',ax=ax4,histtype='step',normed=True,color='r',linewidth=3.0,label='Combined match \n(%d sources)' %len(comb_match))

#rc('text', usetex=True)
#rc('font', family='serif')

for ax,label in zip([ax1,ax2,ax3,ax4],[r'$(a)$',r'$(b)$',r'$(c)$',r'$(d)$']):
	ax.set_xlabel('Spectral Index', fontsize=20)
	ax.set_ylabel('Number of sources (normed)', fontsize=20)
	ax.legend(loc='best',prop={'size':18})
	ax.axvline(x=-0.8,color='k',linestyle='--')
	ax.text(0.05, 0.95, label, transform=ax.transAxes, fontsize=28,
        verticalalignment='top')#, bbox=dict(boxstyle='none'))
	ax.tick_params(labelsize=16)
	


#-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

#good_fit_fluxs = [source.f180_ext for source in sources if source.low_resid==0]
#bad_fit_fluxs = [source.f180_ext for source in sources if source.low_resid==1]


#fig1 = plt.figure()

#ax1 = fig1.add_subplot(231)
#ax1.scatter(good_fit_fluxs,good_fit_SIs,marker='^',s=10,color='r',label='good fit - %d sources' %len(good_fit_fluxs))
#ax1.scatter(bad_fit_fluxs,bad_fit_SIs,marker='s',s=10,color='b',label='bad fit - %d sources' %len(bad_fit_fluxs))
#ax1.set_xlim(-1,60)
#ax1.set_ylim(-2.5,1)
#ax1.set_xlabel('S_180_extrap')
#ax1.set_ylabel('SI')
#ax1.legend(loc='best')

#def plot_search(criteria,colour,marker,label,ax):
	#ax.scatter([source.f180_ext for source in sources if source.num_match==criteria],[source.SI for source in sources if source.num_match==criteria],
		#marker=marker,s=13,color=colour,label=label+' %d sources' %len([source.f180_ext for source in sources if source.num_match==criteria]))

#ax2 = fig1.add_subplot(232)
#ax3 = fig1.add_subplot(233)
#ax4 = fig1.add_subplot(234)
#ax5 = fig1.add_subplot(235)
#ax6 = fig1.add_subplot(236)
#plot_search(1,'k','o','1 match:',ax2)
#plot_search(2,'r','s','2 match:',ax3)
#plot_search(3,'b','^','3 match:',ax4)
#plot_search(4,'g','*','4 match:',ax5)
#plot_search(5,'m','D','5 match:',ax6)
##plot_search(6,'c','p','6 match:')

#def make_lims(ax):
	#ax.set_xlim(-1,60)
	#ax.set_ylim(-2.5,1)
	#ax.set_xlabel('S_180_extrap')
	#ax.set_ylabel('SI')
	#ax.legend(loc='best')
	
#make_lims(ax2)
#make_lims(ax3)
#make_lims(ax4)
#make_lims(ax5)
#make_lims(ax6)


plt.show()