from django.utils.translation import ugettext_lazy as _
from django.shortcuts import render
import simpy


class Option(object):
    def __init__(self, env, ticker, bcs):
        self.ticker = ticker
        self.bcs = bcs
        self.env = env
        self.charge_duration = 5
        self.action = env.process(self.run())
        # self.env.process(self.driver())

    def run(self):
        while True:
            # print('Start parking and charging at %d' % self.env.now)
            try:
                yield self.env.process(self.charge())
            except simpy.Interrupt:
                pass
                # print('Was interrupted. Hope, the battery is full enough ... ' + str(self.env.now))
            # print('Start driving at %d' % self.env.now)
            trip_duration = 2
            yield self.env.timeout(trip_duration)

    def charge(self):
        with self.bcs.request() as req:
            yield req
            yield self.env.timeout(self.charge_duration)

    def driver(self):
        yield self.env.timeout(3)
        self.action.interrupt()


def sim_home(request):
    title = _('Trades Sim App working fine')
    env = simpy.Environment()
    bcs = simpy.Resource(env, capacity=2)
    for i in range(5):
        Option(env, 'TSLA-' + str(i), bcs)
    env.run(until=150)
    return render(request, 'trades/sim_home.html', {'title': title})