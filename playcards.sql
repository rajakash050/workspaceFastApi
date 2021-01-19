-- SQL Dump
-- version 5.0.2

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `playcards`
--

-- --------------------------------------------------------

--
-- Table structure for table `playdetails`
--

CREATE TABLE `playdetails` (
  `autoid` int(11) NOT NULL,
  `uid` int(11) NOT NULL,
  `score` int(11) NOT NULL DEFAULT 0,
  `cardlist` varchar(255) DEFAULT NULL,
  `clickedCards` varchar(255) NOT NULL DEFAULT '{}',
  `prevclicknum` tinyint(2) NOT NULL,
  `createdAt` timestamp NOT NULL DEFAULT current_timestamp(),
  `updatedAt` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `usertoken`
--

CREATE TABLE `usertoken` (
  `autoid` int(11) NOT NULL,
  `uid` int(11) NOT NULL,
  `token` varchar(15) NOT NULL,
  `expiry` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `createdAt` timestamp NOT NULL DEFAULT current_timestamp(),
  `updatedAt` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `playdetails`
--
ALTER TABLE `playdetails`
  ADD PRIMARY KEY (`autoid`) USING BTREE;

--
-- Indexes for table `usertoken`
--
ALTER TABLE `usertoken`
  ADD PRIMARY KEY (`autoid`),
  ADD UNIQUE KEY `uid` (`uid`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `usertoken`
--
ALTER TABLE `usertoken`
  MODIFY `autoid` int(11) NOT NULL AUTO_INCREMENT;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
