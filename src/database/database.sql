/*
 Navicat MySQL Data Transfer

 Source Server         : 本机mysql
 Source Server Type    : MySQL
 Source Server Version : 80032
 Source Host           : localhost:3306
 Source Schema         : finovasystem

 Target Server Type    : MySQL
 Target Server Version : 80032
 File Encoding         : 65001

 Date: 23/04/2023 10:44:29
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for analyzechart
-- ----------------------------
DROP TABLE IF EXISTS `analyzechart`;
CREATE TABLE `analyzechart`  (
  `aid` int NOT NULL AUTO_INCREMENT,
  `analyze_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bg_0900_ai_ci NOT NULL,
  `state` int UNSIGNED NOT NULL,
  `buy_path` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bg_0900_ai_ci NOT NULL,
  `sell_path` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bg_0900_ai_ci NOT NULL,
  `alg_num` int UNSIGNED NOT NULL,
  `stock_num` int UNSIGNED NOT NULL,
  PRIMARY KEY (`aid`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 12 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_bg_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for uploadfile
-- ----------------------------
DROP TABLE IF EXISTS `uploadfile`;
CREATE TABLE `uploadfile`  (
  `fid` int NOT NULL AUTO_INCREMENT,
  `file_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bg_0900_ai_ci NULL DEFAULT NULL,
  `type` int NULL DEFAULT NULL,
  `file_num` int NULL DEFAULT NULL,
  `file_path` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bg_0900_ai_ci NULL DEFAULT NULL,
  `uid` int NULL DEFAULT NULL,
  PRIMARY KEY (`fid`) USING BTREE,
  INDEX `uid`(`uid`) USING BTREE,
  CONSTRAINT `uid` FOREIGN KEY (`uid`) REFERENCES `user` (`uid`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE = InnoDB AUTO_INCREMENT = 21 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_bg_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for user
-- ----------------------------
DROP TABLE IF EXISTS `user`;
CREATE TABLE `user`  (
  `uid` int NOT NULL AUTO_INCREMENT,
  `username` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bg_0900_ai_ci NULL DEFAULT NULL,
  `password` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bg_0900_ai_ci NULL DEFAULT NULL,
  `phoneNumber` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bg_0900_ai_ci NULL DEFAULT NULL,
  `image` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bg_0900_ai_ci NULL DEFAULT NULL,
  PRIMARY KEY (`uid`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 4 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_bg_0900_ai_ci ROW_FORMAT = Dynamic;

SET FOREIGN_KEY_CHECKS = 1;
