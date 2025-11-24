--
-- Base de datos: `vensimweb`
--
CREATE DATABASE IF NOT EXISTS vensimweb;

CREATE USER IF NOT EXISTS 'tcordova'@'localhost' IDENTIFIED BY '123456789';

GRANT ALL PRIVILEGES ON *.* TO 'tcordova'@'localhost';

FLUSH PRIVILEGES;

USE vensimWeb;

CREATE TABLE IF NOT EXISTS `color` (
  `idColor` int(10) NOT NULL,
  `nameColor` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

INSERT IGNORE INTO `color` (`idColor`, `nameColor`) VALUES
(1, '#1f77b4'),
(8, 'black'),
(2, 'blue'),
(5, 'cyan'),
(3, 'green'),
(6, 'magenta'),
(4, 'red'),
(9, 'white'),
(7, 'yellow');

CREATE TABLE IF NOT EXISTS `model` (
  `idModel` int(10) NOT NULL,
  `title` varchar(200) NOT NULL,
  `nameLabelX` varchar(200) NOT NULL,
  `nameLabelY` varchar(200) NOT NULL,
  `position` int(1) NOT NULL DEFAULT 0,
  `nameNivel` varchar(200) NOT NULL,
  `idColor` int(10) NOT NULL DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

INSERT IGNORE INTO `model` (`idModel`, `title`, `nameLabelX`, `nameLabelY`, `position`, `nameNivel`, `idColor`) VALUES
(1, 'Comportamiento del Sistema de Transporte', 'Años', 'N° de Vehiculos', 0, 'transporte', 1),
(2, 'Comportamiento del Sistema de Omnibuses', 'Años', 'N° de Omnibus', 1, 'omnibus', 3),
(3, 'Comportamiento del Sistema de Taxis', 'Años', 'N° de Taxis', 2, 'taxis', 7),
(4, 'Comportamiento del Sistema de Motos', 'Años', 'N° de Motos', 3, 'motos', 4);

ALTER TABLE `color`
  ADD PRIMARY KEY (`idColor`),
  ADD UNIQUE KEY `nameColor` (`nameColor`);

ALTER TABLE `model`
  ADD PRIMARY KEY (`idModel`),
  ADD UNIQUE KEY `nameNivel` (`nameNivel`),
  ADD KEY `model_color` (`idColor`);

ALTER TABLE `color`
  MODIFY `idColor` int(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

ALTER TABLE `model`
  MODIFY `idModel` int(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

ALTER TABLE `model`
  ADD CONSTRAINT `model_color` FOREIGN KEY (`idColor`) REFERENCES `color` (`idColor`);
COMMIT;