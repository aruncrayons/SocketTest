-import os
-from datetime import datetime
-from sqlalchemy import asc, desc, func
-from collections import OrderedDict
+from flask_login import login_required
+from sqlalchemy import asc, desc
+
 from Project import db, csrf
 from Project.Models import (
-    Country, Vehicletype, Admin,
-    Driver, Customer, TermsAndCondition,
-    VehicleGallery, TokenBlacklist,
-    Booking, SetPrice, ParcelMaxWeight,
-    VehicleMaxDistance, Legal, Roles
+    Country, Driver, VehicleGallery, Roles
 )
-from werkzeug.security import check_password_hash, generate_password_hash
-from flask_login import login_required, current_user
+from Project.path_config import DRIVER_INSURANCE_DOCUMENT, DRIVER_TRANSPORT_LICENSE
 from werkzeug.utils import secure_filename
-from Project.path_config import ICON_IMAGES
+import uuid, os
 
 ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'svg'}
-ICON_UPLOAD_FOLDER = ICON_IMAGES
+# ICON_UPLOAD_FOLDER = ICON_IMAGES
 
 
 def allowed_file(filename):
@@ -39,6 +35,7 @@ admin_driver_bp = Blueprint(
     static_folder='admin_static'
 )
 
+
 @admin_driver_bp.context_processor
 def inject_now():
     private_role = Roles.query.filter_by(name='Private').first()
@@ -52,17 +49,16 @@ def admin_ajax_driver(verification_code, user_role):
     # all_driver_details = Driver.find_all()
     start = request.args.get("start", type=int)
     all_driver_details = Driver.query.filter(
-        Driver.verified==verification_code, Driver.delete_driver!=1, Driver.role_id==user_role).order_by(desc(Driver.id))[start:start+10]
-    driver_count = Driver.query.filter(Driver.verified==verification_code, Driver.delete_driver!=1, Driver.role_id==user_role).count()
+        Driver.verified == verification_code, Driver.delete_driver != 1, Driver.role_id == user_role).order_by(
+        desc(Driver.id))[start:start + 10]
+    driver_count = Driver.query.filter(Driver.verified == verification_code, Driver.delete_driver != 1,
+                                       Driver.role_id == user_role).count()
     # print(driver_count)
-    driver_details = [driver_details.to_dict_for_unverified()
+    driver_details = [driver_details.to_dict()
                       for driver_details in all_driver_details]
-    data_dict = {}
+    data_dict = {'recordsTotal': driver_count, 'recordsFiltered': driver_count, 'data': driver_details}
     # data_dict['draw'] = 5
     # data_dict['pageLength'] = 10
-    data_dict['recordsTotal'] = driver_count
-    data_dict['recordsFiltered'] = driver_count
-    data_dict['data'] = driver_details
     # print(data_dict)
 
     if request.args.get("order[0][dir]") != "":
@@ -71,8 +67,9 @@ def admin_ajax_driver(verification_code, user_role):
         # print(request.args.get("order[0][dir]"))
         if request.args.get("order[0][dir]") == "desc":
             all_driver_details = Driver.query.filter(
-                Driver.verified==verification_code, Driver.delete_driver!=1, Driver.role_id==user_role).order_by(asc(Driver.username))[start:start+10]
-            driver_details = [driver_details.to_dict_for_unverified()
+                Driver.verified == verification_code, Driver.delete_driver != 1, Driver.role_id == user_role).order_by(
+                asc(Driver.username))[start:start + 10]
+            driver_details = [driver_details.to_dict()
                               for driver_details in all_driver_details]
             # data_dict['draw'] = 1
             data_dict['data'] = driver_details
@@ -83,51 +80,15 @@ def admin_ajax_driver(verification_code, user_role):
         # print("\n\n\n\n\n\n\n")
         # print(uname)
         if uname is not None:
-            all_driver_details = Driver.query.filter(Driver.verified==verification_code, Driver.delete_driver!=1,
-                Driver.username.ilike('%'+uname+'%'), Driver.verified == verification_code, Driver.role_id==user_role).all()[start:start+10]
-            driver_details = [driver_details.to_dict_for_unverified()
-                              for driver_details in all_driver_details]
-            data_dict['data'] = driver_details
-            data_dict['recordsTotal'] = len(data_dict['data'])
-            data_dict['recordsFiltered'] = len(data_dict['data'])
-    return jsonify(data_dict)
-
-    if request.args.get("order[0][dir]") != "":
-        # print("hai")
-        # print("\n\n\n\n\n\n\n")
-        # print(request.args.get("order[0][dir]"))
-        if request.args.get("order[0][dir]") == "asc":
-            all_driver_details = Driver.query.filter(
-                Driver.verified==verification_code, Driver.role_id==user_role).order_by(asc(Driver.username))
-            driver_details = [driver_details.to_dict()
-                              for driver_details in all_driver_details]
-            # data_dict['draw'] = 1
-            # data_dict['pageLength'] = 10
-            data_dict['data'] = driver_details
-            data_dict['recordsTotal'] = len(data_dict['data'])
-            data_dict['recordsFiltered'] = 10
-        else:
-            all_driver_details = Driver.query.filter(
-                Driver.verified==verification_code, Driver.role_id==user_role).order_by(desc(Driver.username))
+            all_driver_details = Driver.query.filter(Driver.verified == verification_code, Driver.delete_driver != 1,
+                                                     Driver.username.ilike('%' + uname + '%'),
+                                                     Driver.verified == verification_code,
+                                                     Driver.role_id == user_role).all()[start:start + 10]
             driver_details = [driver_details.to_dict()
                               for driver_details in all_driver_details]
-            # data_dict['draw'] = 1
             data_dict['data'] = driver_details
             data_dict['recordsTotal'] = len(data_dict['data'])
-            data_dict['recordsFiltered'] = 10
-        # print(request.args.get("order[0][dir]"))
-    if request.args.get("search[value]") != "":
-        uname = request.args.get("search[value]")
-        # print("\n\n\n\n\n\n\n")
-        # print(uname)
-        all_driver_details = Driver.query.filter(verified==verification_code, Driver.delete_driver!=1, Driver.role_id==user_role,
-            Driver.username.ilike('%'+uname+'%')).all()
-        driver_details = [driver_details.to_dict()
-                          for driver_details in all_driver_details]
-        data_dict['data'] = driver_details
-        data_dict['recordsTotal'] = len(data_dict['data'])
-        data_dict['recordsFiltered'] = 10
-
+            data_dict['recordsFiltered'] = len(data_dict['data'])
     return jsonify(data_dict)
 
 
@@ -145,19 +106,15 @@ def admin_details_driver():
     # print(request.referrer)
     if request.referrer is not None:
         if request.referrer.split('/')[-1] == 'verify_driver':
-            driver_active = True
-            driver_verified_active = False
-            driver_rejected_active = False
+            driver_active, driver_verified_active, driver_rejected_active = True, False, False
         if request.referrer.split('/')[-1] == 'verified_drivers':
-            driver_active = False
-            driver_verified_active = True
-            driver_rejected_active = False
+            driver_active, driver_verified_active, driver_rejected_active = False, True, False
         if request.referrer.split('/')[-1] == 'rejected_drivers':
-            driver_active = False
-            driver_verified_active = False
-            driver_rejected_active = True
+            driver_active, driver_verified_active, driver_rejected_active = False, False, True
 
-    return render_template('admin_driver_details.html', driver=driver, vehicle_images=vehicle_images, driver_active=driver_active, driver_verified_active=driver_verified_active, driver_rejected_active=driver_rejected_active)
+    return render_template('admin_driver_details.html', driver=driver, vehicle_images=vehicle_images,
+                           driver_active=driver_active, driver_verified_active=driver_verified_active,
+                           driver_rejected_active=driver_rejected_active)
 
 
 @admin_driver_bp.route('/verify_driver', methods=["GET", "POST"])
@@ -209,12 +166,6 @@ def admin_remove_driver():
     return redirect(url_for('admin_driver_bp.all_driver'))
 
 
-@admin_driver_bp.route('/edit_drivers', methods=["GET", "POST"])
-@login_required
-def admin_update_driver():
-    return redirect(url_for('admin_driver_bp.all_driver'))
-
-
 @admin_driver_bp.route('/accept_driver', methods=["GET"])
 @login_required
 def admin_accept_driver():
@@ -241,3 +192,71 @@ def admin_reject_driver():
     flash(f"Rejected {driver.username} Successfully...")
     # return redirect(url_for('admin.all_driver'))
     return redirect(url_for('admin_driver_bp.all_rejected_drivers'))
+
+
+@admin_driver_bp.route('/edit_drivers', methods=["GET", "POST"])
+@login_required
+def admin_update_driver():
+    user_id = request.args.get('user_id')
+    driver_details = Driver.find_by_id(user_id)
+    driver_active, driver_verified_active, driver_rejected_active = False, False, False
+    if request.referrer is not None:
+        if request.referrer.split('/')[-1] == 'verify_driver':
+            driver_active, driver_verified_active, driver_rejected_active = True, False, False
+        if request.referrer.split('/')[-1] == 'verified_drivers':
+            driver_active, driver_verified_active, driver_rejected_active = False, True, False
+        if request.referrer.split('/')[-1] == 'rejected_drivers':
+            driver_active, driver_verified_active, driver_rejected_active = False, False, True
+    return render_template('admin_edit_driver.html', u_driver=driver_details, driver_active=driver_active,
+                           driver_verified_active=driver_verified_active, driver_rejected_active=driver_rejected_active)
+
+
+@admin_driver_bp.route('/upgrade_driver_to_company', methods=['GET', 'POST'])
+@login_required
+def admin_upgrade_driver_to_company():
+    driver_id = request.args.get('driver_id')
+    driver_details = Driver.find_by_id(driver_id)
+
+    if request.method == "POST":
+        company_name = request.form.get('txt_company_name')
+        reg_num = request.form.get('txt_reg_num')
+        vat_tax_identification = request.form.get('txt_vat_tax_identification')
+        identification_number = request.form.get('txt_identification_number')
+        hidden_driver_id = request.form.get('hidden_driver_id')
+        if 'insurance_doc' and 'transport_license' not in request.files:
+            flash('Please choose file for upload')
+            return redirect(url_for('admin_driver_bp.admin_upgrade_driver_to_company', driver_id=hidden_driver_id))
+        insurance_doc = request.files['insurance_doc']
+        transport_license = request.files['transport_license']
+        if insurance_doc and allowed_file(insurance_doc.filename):
+            file_name, extension = os.path.splitext(insurance_doc.filename)
+            insurance_doc.filename = str(uuid.uuid4()) + f'.{extension}'
+            filename1 = secure_filename(insurance_doc.filename)
+            print(filename1)
+            insurance_doc.save(os.path.join(DRIVER_INSURANCE_DOCUMENT, filename1))
+
+        if transport_license and allowed_file(transport_license.filename):
+            file_name, extension = os.path.splitext(transport_license.filename)
+            transport_license.filename = str(uuid.uuid4()) + f'.{extension}'
+            filename2 = secure_filename(transport_license.filename)
+            print(filename2)
+            transport_license.save(os.path.join(DRIVER_TRANSPORT_LICENSE, filename2))
+
+        role_details = Roles.query.filter_by(name='Company').first()
+        upgrade_courier = Driver.find_by_id(hidden_driver_id)
+
+        upgrade_courier.role_id = role_details.id
+        upgrade_courier.company_name = company_name
+        upgrade_courier.vat_tax_identification = vat_tax_identification
+        upgrade_courier.registration_number = reg_num
+        upgrade_courier.insurance_document = filename1
+        upgrade_courier.transport_license = filename2
+        upgrade_courier.save_to_db()
+        return redirect(url_for('admin_company_driver_bp.all_verified_company_drivers'))
+
+
+    driver_active, driver_verified_active, driver_rejected_active = False, True, False
+    return render_template('admin_upgrade_driver_to_company.html', driver_details=driver_details,
+                           driver_active=driver_active, driver_verified_active=driver_verified_active,
+                           driver_rejected_active=driver_rejected_active)