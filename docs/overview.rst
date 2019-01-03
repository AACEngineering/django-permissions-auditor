Overview
========

In large Django applications that require complex access control, it can be difficult
for site administrators to effectively assign and manage permissions for users and groups.

I often found that I needed to reference my site's source code in order to remember
what permission was required for what view - something end-users and managers shouldn't
need to do.

Django-permissions-auditor attempts to solve this problem by automatically parsing
out permissions so that administrators can easily manage their site.
