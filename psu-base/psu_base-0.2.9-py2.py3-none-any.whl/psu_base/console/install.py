import os
import fileinput
import inspect
import subprocess
from psu_base.console import out
import psu_base.templates.app_settings_template
import psu_base.templates.local_settings_template
from  psu_base.templates.gitignore_template import content as gitignore_template


def run_install():
    # Must be in project root
    if not os.path.isfile('manage.py'):
        print(f"\n\nYou must run the install script from your Django project's root directory\n")
        return False

    # Determine app directory
    dirs = [dd for dd in os.listdir() if os.path.isdir(dd) and not dd.startswith('.')]
    app_dir = None
    if len(dirs) == 1:
        app_dir = dirs[0]
    elif len(dirs) > 1:
        app_dir = out.prompt("Which directory is your app in?", dirs, None, False)

    # App directory must have been found to continue
    if not app_dir:
        print(f"\n\nCould not determine your app's directory\n")
        return False

    has_errors = False

    # Prepare file paths for editing
    settings_file = os.path.join(app_dir, 'settings.py')
    app_settings_file = os.path.join(app_dir, 'app_settings.py')
    local_settings_file = os.path.join(app_dir, 'local_settings.py')
    urls_file = os.path.join(app_dir, 'urls.py')

    # ###########################################
    # Edit settings.py
    # ###########################################
    added_installed_apps = False
    added_imports = False
    try:
        sf = fileinput.FileInput(settings_file, inplace=True, backup='.bak')
        in_installed_apps = False
        for line in sf:
            # Mark the beginning of installed_apps list
            if not in_installed_apps and line.startswith('INSTALLED_APPS'):
                in_installed_apps = True

            # Wait for the end of the installed_apps list
            if in_installed_apps and ']' in line:
                # Add psu_base and others
                print('    #')
                print("    'django_cas_ng',")
                print("    'crequest',")
                print("    'psu_base',")
                added_installed_apps = True

                # This ends the INSTALLED_APPS section
                in_installed_apps = False

            # Print the original line back to the file
            print(line.strip("\n"))

        # Close the file and remove the backup
        sf.close()
        os.unlink(f"{settings_file}.bak")

    except Exception as ee:
        has_errors = True
        out.print_color(f"Could not modify {settings_file}: {str(ee)}", 'red')

    if not added_installed_apps:
        has_errors = True
        out.print_color("Unable to append to INSTALLED_APPS", 'red')
        print("You must manually add django_cas_ng, crequest, and psu-base to your INSTALLED_APPS list")

    try:
        # Add imports to the end of the file
        with open(settings_file, "a") as set_f:
            set_f.write("""
# Get app-specific settings
from .app_settings import *

# Override settings with values for the local environment
from .local_settings import *\n""")
        added_imports = True
    except Exception as ee:
        has_errors = True
        out.print_color(f"Could not import app and local settings in {settings_file}: {str(ee)}", 'red')

    # ###########################################
    # Edit urls.py
    # ###########################################
    added_urls = False
    try:
        in_imports = False
        sf = fileinput.FileInput(urls_file, inplace=True, backup='.bak')
        for line in sf:
            # Have to add imports
            if line.startswith('from'):
                in_imports = True
            elif in_imports:
                # Time to add new imports
                print("""\
from django.conf import settings
from django.conf.urls import url
from django.views.generic import RedirectView
import psu_base.views as psu_views
from django.urls import path, include\n""")
                in_imports = False

            # Replace the admin definition (should be the only one in the initial file)
            if 'admin.site.urls' in line:
                print("""\
    # On-prem apps will have additional URL context
    path('', RedirectView.as_view(url='/'+settings.URL_CONTEXT)),

    # Django admin site. Probably won't use this. Our apps typically use Banner security classes.
    # Finti's sso_proxy app has JWT-specific permission endpoints that could be modified for service-to-service calls
    path(settings.URL_CONTEXT + '/admin/', admin.site.urls),\n""")
                # Do not print the original line
                continue

            # Wait for the end of the URL list
            if ']' in line:
                print("""\
    # PSU and CAS views are defined in psu_base app
    url(settings.URL_CONTEXT+'/psu/', include(('psu_base.urls', 'psu_base'), namespace='psu')),
    url(settings.URL_CONTEXT+'/accounts/', include(('psu_base.urls', 'psu_base'), namespace='cas')),
    
    # Use status as initial view
    path(settings.URL_CONTEXT + '/', psu_views.test_status, name='home'),""")

            # Print the original line back to the file
            print(line.strip("\n"))
        # Close the file and remove the backup
        sf.close()
        os.unlink(f"{urls_file}.bak")

        added_urls = True

    except Exception as ee:
        has_errors = True
        out.print_color(f"Could not modify {urls_file}: {str(ee)}", 'red')

    if not added_urls:
        has_errors = True
        out.print_color("Unable to append to urls.py", 'red')
        print("You must manually add PSU and CAS URLs")

    # ###########################################
    # Copy template files into new project
    # ###########################################
    try:
        app_settings = inspect.getsource(psu_base.templates.app_settings_template)
        with open(app_settings_file, 'w+') as app_f:
            app_f.write(app_settings)
    except Exception as ee:
        has_errors = True
        out.print_color(f"Could not modify {app_settings_file}: {str(ee)}", 'red')

    try:
        local_settings = inspect.getsource(psu_base.templates.local_settings_template)
        with open(local_settings_file, 'w+') as app_f:
            app_f.write(local_settings)
    except Exception as ee:
        has_errors = True
        out.print_color(f"Could not modify {local_settings_file}: {str(ee)}", 'red')

    try:
        with open('.gitignore', 'w+') as app_f:
            app_f.write(gitignore_template.strip())
    except Exception as ee:
        has_errors = True
        out.print_color(f"Could not modify .gitignore: {str(ee)}", 'red')

    # ###########################################
    # Prompt for app-specific values
    # ###########################################
    app_code = out.prompt("Enter a unique code for your app (i.e. DEMO, PETITION): ", make_uppercase=True)
    app_name = out.prompt("Enter a name for your app (i.e. 'DAC Petition'): ")
    finti_token = out.prompt("Enter your Finti token: ")

    # ###########################################
    # Edit app_settings.py
    # ###########################################
    added_app_code = False
    if app_name or app_code:
        try:
            sf = fileinput.FileInput(app_settings_file, inplace=True, backup='.bak')
            for line in sf:
                # Have to add imports
                if line.startswith('APP_CODE' and app_code):
                    print(f"APP_CODE = '{app_code}'")
                    added_app_code = True
                    continue

                elif line.startswith('APP_NAME' and app_name):
                    print(f"APP_NAME = '{app_name}'")
                    continue

                # Print the original line back to the file
                print(line.strip("\n"))
            # Close the file and remove the backup
            sf.close()
            os.unlink(f"{app_settings_file}.bak")

        except Exception as ee:
            has_errors = True
            out.print_color(f"Could not modify {app_settings_file}: {str(ee)}", 'red')

    # ###########################################
    # Edit local_settings.py
    # ###########################################
    added_finti_token = False
    if finti_token:
        try:
            sf = fileinput.FileInput(local_settings_file, inplace=True, backup='.bak')
            for line in sf:
                # Have to add imports
                if line.startswith('FINTI_TOKEN' and finti_token):
                    print(f"FINTI_TOKEN = '{finti_token}'")
                    added_finti_token = True
                    continue

                # Print the original line back to the file
                print(line.strip("\n"))
            # Close the file and remove the backup
            sf.close()
            os.unlink(f"{local_settings_file}.bak")

        except Exception as ee:
            has_errors = True
            out.print_color(f"Could not modify {local_settings_file}: {str(ee)}", 'red')

    # ###########################################
    # Other setup functions...
    # ###########################################

    # Make the logs directory
    if not os.path.isdir('logs'):
        os.mkdir('logs')

    # Run migrations
    ran_migrations = False
    try:
        subprocess.run(["python", "manage.py", "migrate"])
        ran_migrations = True
    except Exception as ee:
        out.print_color(f"Error running migrations: {str(ee)}", 'red')

    # ###########################################
    # Print instructions, as best as possible
    # ###########################################
    if not has_errors:
        print("App successfully started!\n\nNext Steps:")

        ii = 1
        if not added_app_code:
            print(f"\t{ii}. Open {app_settings_file} and enter app-specific data")
            ii += 1
        if not added_finti_token:
            print(f"\t{ii}. Open {local_settings_file} and enter your Finti token")
            ii += 1
        if not ran_migrations:
            print(f"\t{ii}. Run migrations ( python manage.py migrate )")
            ii += 1

        if ii > 1:
            print(f"\t{ii} python manage.py runserver localhost:8000")
        else:
            print("\tpython manage.py runserver localhost:8000")

    else:
        print(f"""

Some errors occurred!

Review any error messages that might tell you what needs to be done.

When in doubt, read the Confluence documentation at 
https://portlandstate.atlassian.net/wiki/spaces/WDT/pages/728662545/PSU+Base+Plugin+Installation.
        """)

    return not has_errors
