-- phpMyAdmin SQL Dump
-- version 4.9.0.1
-- https://www.phpmyadmin.net/
--
-- Host: 10.150.1.49
-- Erstellungszeit: 23. Jan 2020 um 11:19
-- Server-Version: 10.3.18-MariaDB-0+deb10u1
-- PHP-Version: 7.4.1

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `bmbf__auth`
--

CREATE TABLE `bmbf__auth` (
  `uid` int(11) NOT NULL,
  `token` varchar(190) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `bmbf__events`
--

CREATE TABLE `bmbf__events` (
  `id` int(11) NOT NULL,
  `organization` mediumtext NOT NULL,
  `measure` mediumtext NOT NULL,
  `template` int(11) NOT NULL,
  `measure_periode` mediumtext NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `bmbf__groups`
--

CREATE TABLE `bmbf__groups` (
  `event` int(11) NOT NULL,
  `group_id` mediumtext NOT NULL,
  `ugid` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `bmbf__mapping`
--

CREATE TABLE `bmbf__mapping` (
  `uid` int(11) NOT NULL,
  `eid` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `bmbf__participants`
--

CREATE TABLE `bmbf__participants` (
  `id` int(11) NOT NULL,
  `event` int(11) NOT NULL,
  `name` mediumtext NOT NULL,
  `university` mediumtext NOT NULL,
  `grp` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `bmbf__templates`
--

CREATE TABLE `bmbf__templates` (
  `id` int(11) NOT NULL,
  `filename` mediumtext NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `bmbf__times`
--

CREATE TABLE `bmbf__times` (
  `event` int(11) NOT NULL,
  `startdate` date NOT NULL,
  `enddate` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Indizes der exportierten Tabellen
--

--
-- Indizes für die Tabelle `bmbf__auth`
--
ALTER TABLE `bmbf__auth`
  ADD PRIMARY KEY (`uid`),
  ADD UNIQUE KEY `bmbf__auth_key_uindex` (`token`);

--
-- Indizes für die Tabelle `bmbf__events`
--
ALTER TABLE `bmbf__events`
  ADD PRIMARY KEY (`id`),
  ADD KEY `bmbf__events_bmbf__templates_id_fk` (`template`);

--
-- Indizes für die Tabelle `bmbf__groups`
--
ALTER TABLE `bmbf__groups`
  ADD PRIMARY KEY (`ugid`),
  ADD KEY `bmbf__groups_bmbf__events_id_fk` (`event`);

--
-- Indizes für die Tabelle `bmbf__mapping`
--
ALTER TABLE `bmbf__mapping`
  ADD UNIQUE KEY `bmbf__mapping_eid_uindex` (`eid`),
  ADD KEY `bmbf__mapping_bmbf__auth_uid_fk` (`uid`);

--
-- Indizes für die Tabelle `bmbf__participants`
--
ALTER TABLE `bmbf__participants`
  ADD PRIMARY KEY (`id`),
  ADD KEY `bmbf__articipants_bmbf__events_id_fk` (`event`),
  ADD KEY `bmbf__participants_bmbf__groups_ugid_fk` (`grp`);

--
-- Indizes für die Tabelle `bmbf__templates`
--
ALTER TABLE `bmbf__templates`
  ADD PRIMARY KEY (`id`);

--
-- Indizes für die Tabelle `bmbf__times`
--
ALTER TABLE `bmbf__times`
  ADD KEY `bmbf__times_bmbf__events_id_fk` (`event`);

--
-- AUTO_INCREMENT für exportierte Tabellen
--

--
-- AUTO_INCREMENT für Tabelle `bmbf__auth`
--
ALTER TABLE `bmbf__auth`
  MODIFY `uid` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT für Tabelle `bmbf__events`
--
ALTER TABLE `bmbf__events`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT für Tabelle `bmbf__groups`
--
ALTER TABLE `bmbf__groups`
  MODIFY `ugid` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT für Tabelle `bmbf__participants`
--
ALTER TABLE `bmbf__participants`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT für Tabelle `bmbf__templates`
--
ALTER TABLE `bmbf__templates`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- Constraints der exportierten Tabellen
--

--
-- Constraints der Tabelle `bmbf__events`
--
ALTER TABLE `bmbf__events`
  ADD CONSTRAINT `bmbf__events_bmbf__templates_id_fk` FOREIGN KEY (`template`) REFERENCES `bmbf__templates` (`id`);

--
-- Constraints der Tabelle `bmbf__groups`
--
ALTER TABLE `bmbf__groups`
  ADD CONSTRAINT `bmbf__groups_bmbf__events_id_fk` FOREIGN KEY (`event`) REFERENCES `bmbf__events` (`id`);

--
-- Constraints der Tabelle `bmbf__mapping`
--
ALTER TABLE `bmbf__mapping`
  ADD CONSTRAINT `bmbf__mapping_bmbf__auth_uid_fk` FOREIGN KEY (`uid`) REFERENCES `bmbf__auth` (`uid`),
  ADD CONSTRAINT `bmbf__mapping_bmbf__events_id_fk` FOREIGN KEY (`eid`) REFERENCES `bmbf__events` (`id`);

--
-- Constraints der Tabelle `bmbf__participants`
--
ALTER TABLE `bmbf__participants`
  ADD CONSTRAINT `bmbf__articipants_bmbf__events_id_fk` FOREIGN KEY (`event`) REFERENCES `bmbf__events` (`id`),
  ADD CONSTRAINT `bmbf__participants_bmbf__groups_ugid_fk` FOREIGN KEY (`grp`) REFERENCES `bmbf__groups` (`ugid`);

--
-- Constraints der Tabelle `bmbf__times`
--
ALTER TABLE `bmbf__times`
  ADD CONSTRAINT `bmbf__times_bmbf__events_id_fk` FOREIGN KEY (`event`) REFERENCES `bmbf__events` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
