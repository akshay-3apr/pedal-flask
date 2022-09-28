from app.models import Users,load_user

def check_loggedInUser(user):
    # fetch logged-in user role
    user = Users.query.filter_by(username=user.username).first()
    if user.role.lower() == "customer":
        sideBarItems = [
            {
                'item': "Dashboard",
                'active': True,
                'icon': 'fa-map-marker-alt',
                'url': 'load_dash'
            },
            {
                'item': "Previous Trips",
                'active': False,
                'icon': 'fa-biking',
                'url': 'payment'  # 'load_previousTrips'
            },
            {
                'item': "Report Defect",
                'active': False,
                'icon': 'fa-info-circle',
                'url': 'defectiveBikes'  # 'load_reportDefect'
            }
        ]
        navBarItems = [
            {
                'item': "Home",
                'active': True,
                'url': 'load_dash'
            },
            {
                'item': "Payment",
                'active': False,
                'url': 'payment'
            }
        ]
    elif user.role.lower() == "operator":
        sideBarItems = [
            {
                'item': "Dashboard",
                'active': True,
                'icon': 'fa-map-marker-alt',
                'url': 'load_dash'
            },
            {
                'item': "Move Cycles",
                'active': False,
                'icon': 'fa-biking',
                'url': 'manageCycles'
            },
            {
                'item': "Manage Defect",
                'active': False,
                'icon': 'fa-info-circle',
                'url': 'repairBikes'  # 'load_reportDefect'
            }
        ]
        navBarItems = [
            {
                'item': "Home",
                'active': True,
                'url': 'load_dash'
            }
        ]
    elif user.role.lower() == "manager":
        sideBarItems = [
            {
                'item': "Dashboard",
                'active': True,
                'icon': 'fa-map-marker-alt',
                'url': 'load_manager_charts'
            }
        ]
        navBarItems = [
            {
                'item': "Home",
                'active': True,
                'url': 'load_manager_charts'
            },
            {
                'item': "Load Operator",
                'active': False,
                'url': 'loadOperator'
            }
        ]
    return (sideBarItems,navBarItems)