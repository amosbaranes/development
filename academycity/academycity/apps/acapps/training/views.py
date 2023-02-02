from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from ...webcompanies.WebCompanies import WebSiteCompany
from ...core.utils import log_debug
from django.urls import reverse
from ...core.apps_general_functions import activate_obj_function

def home(request):
    return render(request, 'training//home1.html', {})

k = {
        10: {"title": "War Training", "type": 1, "color": "#ffffe6",
             "sub_tests": {"type": 3, "data":
                 {
                     100010: {"title": "Single War Strip",
                              "questions":
                                  {1: {"title": "grade for Single War Strip"}
                                   }
                              },
                     100020: {"title": "Single Practice",
                              "questions":
                                  {1: {"title": "grade for Single Practice"}
                                   }
                              },
                     100030: {"title": "Field craft",
                              "questions":
                                  {1: {"title": "grade for Field craft"}
                                   }
                              }
                 }
                           }
             },
        20: {"title": "Fitness", "type": 1, "color": "#e6ffff",
             "sub_tests": {"type": 2, "data":
                 {
                     2010: {"title": "Physical Fitness", "type": 2, "color": "blue",
                            "sub_tests": {"type": 3, "data":
                                {
                                    201010: {"title": "Run 300",
                                             "questions":
                                                 {1: {"title": "grade for Run 300"}
                                                  }
                                             },
                                    201020: {"title": "Run 3000",
                                             "questions":
                                                 {1: {"title": "grade for Run 3000"}
                                                  }
                                             },
                                    201030: {"title": "Run 5000",
                                             "questions":
                                                 {1: {"title": "grade for Run 5000"}
                                                  }
                                             },
                                    201040: {"title": "Run 10000",
                                             "questions":
                                                 {1: {"title": "grade for Run 10000"}
                                                  }
                                             },
                                    201050: {"title": "Thick subjugation",
                                             "questions":
                                                 {1: {"title": "grade for Run 10000"}
                                                  }
                                             }
                                }
                                          }
                            },
                     2020: {"title": "Combat Fitness", "type": 2, "color": "blue",
                             "sub_tests": {"type": 3, "data":
                                 {
                                     202010: {"title": "Fighting combat",
                                              "questions":
                                                  {1: {"title": "grade for Fighting combat"}
                                                   }
                                              },
                                     202020: {"title": "Obstacle course",
                                              "questions":
                                                  {1: {"title": "grade for Obstacle course"}
                                                   }
                                              }
                                 }
                                           }
                             },
                     2030: {"title": "Combat Walk", "type": 2, "color": "blue",
                            "sub_tests": {"type": 3, "data":
                                {
                                    203010: {"title": "Getting the weapon",
                                             "questions":
                                                 {1: {"title": "grade for Getting the weapon"}
                                                  }
                                             },
                                    203020: {"title": "Getting the gun",
                                             "questions":
                                                 {1: {"title": "grade for Getting the gun"}
                                                  }
                                             },
                                    203030: {"title": "Pre-Commando",
                                             "questions":
                                                 {1: {"title": "grade for Pre-Commando"}
                                                  }
                                             },
                                    203040: {"title": "Week no 7",
                                             "questions":
                                                 {1: {"title": "grade for Week no 7"}
                                                  }
                                             },
                                    203050: {"title": "Final preparing",
                                             "questions":
                                                 {1: {"title": "grade for Final preparing"}
                                                  }
                                             },
                                    203060: {"title": "Final",
                                             "questions":
                                                 {1: {"title": "grade for Final"}
                                                  }
                                             },
                                }
                                          }
                            }
                 }
                           }
             },
        30: {"title": "Hitting", "type": 1, "color": "#e6e6ff",
             "sub_tests": {"type": 2, "data":
                 {
                     3010: {"title": "Weapon", "type": 2, "color": "blue",
                            "sub_tests": {"type": 3, "data":
                                {
                                    301010: {"title": "Professional use", "type": 3,
                                             "questions":
                                                 {1: {"title": "grade for Professional use"}
                                                  }
                                             },
                                    301020: {"title": "Final Hitting test", "type": 3,
                                             "questions":
                                                 {1: {"title": "grade for Final Hitting test 1"},
                                                  2: {"title": "grade for Final Hitting test 2"}
                                                  }
                                             },
                                    301030: {"title": "Safety", "type": 3,
                                             "questions":
                                                 {1: {"title": "grade for Safety"}
                                                  }
                                             }
                                }
                                          }
                            },
                     3020: {"title": "Gun", "type": 2, "color": "blue",
                            "sub_tests": {"type": 3, "data":
                                {
                                    302010: {"title": "Professional use", "type": 3,
                                            "questions":
                                                {1: {"title": "grade for Professional use"}
                                                 }
                                            },
                                    302020: {"title": "Final Hitting test", "type": 3,
                                            "questions":
                                                {1: {"title": "grade for Final Hitting test 1"},
                                                 2: {"title": "grade for Final Hitting test 2"}
                                                 }
                                            },
                                    302030: {"title": "Safety", "type": 3,
                                            "questions":
                                                {1: {"title": "grade for Safety"}
                                                 }
                                            }
                                }
                                          }
                            }
                 }
                           }
             }
    }

def home(request):
    wsc = WebSiteCompany(request, web_company_id=20)
    company_obj = wsc.site_company()
    company_obj_id_ = company_obj.id
    app_name = "default"
    return app_id(request, app_name, company_obj_id_)

def homet(request):
    wsc = WebSiteCompany(request, web_company_id=20, is_test=True)
    company_obj = wsc.site_company()
    company_obj_id_ = company_obj.id
    app_name = "default"
    return app_id(request, app_name, company_obj_id_)


def app_id(request, app_name, company_obj_id):
    company_obj_id_ = company_obj_id
    app_ = "training"
    app_activate_function_link_ = reverse(app_+':activate_obj_function', kwargs={})
    return render(request, app_+'//home.html', {"atm_name": app_+"_"+app_name+"_atm",
                                                "app": app_,
                                                "app_activate_function_link": app_activate_function_link_,
                                                "company_obj_id": company_obj_id_,
                                                "title": app_}
                  )


def appt(request, app_name):
    wsc = WebSiteCompany(request, web_company_id=20, is_test=True)
    company_obj = wsc.site_company()
    company_obj_id_ = company_obj.id
    return app_id(request, app_name, company_obj_id_)

def app(request, app_name):
    wsc = WebSiteCompany(request)
    company_obj = wsc.site_company()
    company_obj_id_ = company_obj.id
    return app_id(request, app_name, company_obj_id_)
