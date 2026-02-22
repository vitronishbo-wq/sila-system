import { Link } from "react-router-dom";

export default function NotFound() {
  return (
    <div style={{ padding: 40, textAlign: "center" }}>
      <h1>404 - Página não encontrada</h1>
      <p>A página que você procura não existe.</p>
      <Link to="/" style={{ marginTop: 20, display: "inline-block" }}>
        Voltar ao Início
      </Link>
    </div>
  );
}
