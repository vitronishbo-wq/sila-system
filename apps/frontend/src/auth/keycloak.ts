import Keycloak from "keycloak-js"

const keycloak = new Keycloak({
  url: "http://localhost:8081",
  realm: "portal-nacional",
  clientId: "portal-frontend"
})

export default keycloak
