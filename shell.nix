{ pkgs ? import <nixpkgs> {} }:
(pkgs.python3.withPackages (p: with p; [
	python-dotenv
	twilio
	(selenium.overrideAttrs(old: rec {
		postInstall = ''
		install -Dm 755 ../rb/lib/selenium/webdriver/atoms/getAttribute.js $out/${python.sitePackages}/selenium/webdriver/remote/getAttribute.js
		install -Dm 755 ../rb/lib/selenium/webdriver/atoms/isDisplayed.js $out/${python.sitePackages}/selenium/webdriver/remote/isDisplayed.js
		'';
	}))
])).env
