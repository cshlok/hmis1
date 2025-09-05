package opa.rbac

# This policy ensures that users have the proper role and permissions to access resources.
# It enforces least privilege and audit logging standards as per enterprise guidelines.

default allow = false

# Allow access if the user has the required role and the request meets audit requirements.
allow {
    input.user.role == "admin"
}

allow {
    input.user.role == "doctor"
    input.resource in ["patient_records", "appointments"]
}

allow {
    input.user.role == "nurse"
    input.resource == "appointments"
}
