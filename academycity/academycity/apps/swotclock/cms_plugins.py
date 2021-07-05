from django.utils.translation import ugettext_lazy as _
from cms.plugin_base import CMSPluginBase
from cms.models.pluginmodel import CMSPlugin
from cms.plugin_pool import plugin_pool


@plugin_pool.register_plugin
class SWOT(CMSPluginBase):
    model = CMSPlugin  # Model where data about this plugin is saved
    render_template = "swotclock/swotclock.html"  # template to render the plugin with
    name = _("SwotClock")  # Name of the plugin
    cache = False

    def render(self, context, instance, placeholder):
        context = super().render(context, instance, placeholder)
        return context
