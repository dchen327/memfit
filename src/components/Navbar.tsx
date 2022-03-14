export function Navbar() {
  return (
    <nav id="navbar-main" className="navbar is-dark is-fixed-top">
      <div className="navbar-brand">
        <h1 className="title has-text-light p-4">MemFit</h1>
      </div>
      <div className="navbar-menu">
        <div className="navbar-end">
          <div className="navbar-item mr-3">Sign out</div>
        </div>
      </div>
    </nav>
  );
}
