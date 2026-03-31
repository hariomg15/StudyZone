export function saveToken(token) {
  localStorage.setItem("token", token);
}

export function saveUser(user) {
  localStorage.setItem("user", JSON.stringify(user));
}

export function getToken() {
  return localStorage.getItem("token");
}

export function getUser() {
  const rawUser = localStorage.getItem("user");

  if (!rawUser) {
    return null;
  }

  try {
    return JSON.parse(rawUser);
  } catch {
    localStorage.removeItem("user");
    return null;
  }
}

export function isLoggedIn() {
  return Boolean(getToken());
}

export function hasRole(roles = []) {
  const user = getUser();
  return Boolean(user && roles.includes(user.role));
}

export function logout() {
  localStorage.removeItem("token");
  localStorage.removeItem("user");
}
