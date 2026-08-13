Start SHA:
d98ac051b67369adcb1481d33ed52ac43eb3d537

1. Add one canonical auth-transition helper in app.js:
   - navigate to target hash;
   - if navigate() returns false, call router.refresh().

2. Use it for:
   - showLogin()
   - successful/local performLogout()
   - onPasswordChanged()

3. In profile.js passwordForm():
   - when changePassword() fails,
   - first handle Abort/stale route,
   - then call context.handleAuthError(error);
   - if it handles a 401, return without rendering a password error.
   - ordinary 4xx validation/password errors remain on the form.

4. Add deterministic regressions:
   - must_change_password=true while URL already #/login;
   - Sign out results in actual Login view;
   - successful password change results in actual Login view;
   - change-password HTTP 401 clears identity and renders Login;
   - no duplicate route render/cleanup regression.

5. Preserve all Phase 1J.1 behavior.
6. No schema, migration, dependency, backend API, permission or Phase 1K changes.
7. Run full existing quality suite.

End:
Phase 1J.2: PASS — Phase 1K ready for independent review