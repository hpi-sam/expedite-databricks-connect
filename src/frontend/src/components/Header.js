import React from 'react';
import '../App.css'; 

function Header() {
  return (
    <header className="header">
      {/* Grouping left and center sections */}
      <div className="header__left-center">
        <div className="header__left">
        </div>
        <div className="header__center">
          <h1>Master Project: Quickly adapting to changes</h1>
        </div>
      </div>
      <div className="header__right">
        <img id="logo" src="/hpi_logo.png" alt="4flow logo" />
      </div>
    </header>
  );
}

export default Header;
