from django.utils.translation import ugettext_lazy as _
from cms.plugin_base import CMSPluginBase
from cms.models.pluginmodel import CMSPlugin
from cms.plugin_pool import plugin_pool


@plugin_pool.register_plugin
class FSA(CMSPluginBase):
    model = CMSPlugin  # Model where data about this plugin is saved
    render_template = "corporatevaluation/FSA.html"  # template to render the plugin with
    name = _("FSA")  # Name of the plugin
    cache = False


@plugin_pool.register_plugin
class FSA_HV_I(CMSPluginBase):
    model = CMSPlugin  # Model where data about this plugin is saved
    render_template = "corporatevaluation/FSA_HV_I.html"  # template to render the plugin with
    name = _("FSA-HV-I")  # Name of the plugin
    cache = False


@plugin_pool.register_plugin
class FSA_HV_BS(CMSPluginBase):
    model = CMSPlugin  # Model where data about this plugin is saved
    render_template = "corporatevaluation/FSA_HV_B.html"  # template to render the plugin with
    name = _("FSA-HV-BS")  # Name of the plugin
    cache = False


@plugin_pool.register_plugin
class FSA_RATIO(CMSPluginBase):
    model = CMSPlugin  # Model where data about this plugin is saved
    render_template = "corporatevaluation/FSA_RATIO.html"  # template to render the plugin with
    name = _("FSA-RATIO")  # Name of the plugin
    cache = False


@plugin_pool.register_plugin
class WaccEbitRoicPlugin(CMSPluginBase):
    model = CMSPlugin  # Model where data about this plugin is saved
    render_template = "corporatevaluation/wacc_ebit_roic.html"  # template to render the plugin with
    name = _("WaccEbitRoic")  # Name of the plugin
    cache = False


@plugin_pool.register_plugin
class GordonEquationPlugin(CMSPluginBase):
    model = CMSPlugin  # Model where data about this plugin is saved
    render_template = "corporatevaluation/gordon_equation.html"  # template to render the plugin with
    name = _("Gordon Equation")  # Name of the plugin
    cache = False


@plugin_pool.register_plugin
class DCFBasicPlugin(CMSPluginBase):
    model = CMSPlugin  # Model where data about this plugin is saved
    render_template = "corporatevaluation/dcf_basic.html"  # template to render the plugin with
    name = _("DCF-Basic")  # Name of the plugin
    cache = False


@plugin_pool.register_plugin
class EquityEnterpriseValuationPlugin(CMSPluginBase):
    model = CMSPlugin  # Model where data about this plugin is saved
    render_template = "corporatevaluation/equity_enterprise_valuation.html"  # template to render the plugin with
    name = _("EquityEnterpriseValuation")  # Name of the plugin
    cache = False

