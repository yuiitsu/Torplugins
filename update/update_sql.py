# -*- coding: utf-8 -*-

"""
@author: Yuiitsu
@file: update_sql
@time: 2018/7/10 10:14
"""
import os
import tornado.gen
from source.async_model import AsyncModelBase
import version


class Model(AsyncModelBase):

    @tornado.gen.coroutine
    def execute_sql(self):
        """
        执行SQL
            1. 根据版本号获取SQL目录
            2. 获取当前系统的版本
            3. 读取目标目录下的所有文件，按文件拼成SQL并执行
        :return:
        """
        # 1.
        v = version.WM_VERSION
        target_version = int(v.replace(".", ""))

        # 2.
        current_version = target_version
        current_version_result = yield self.find('tbl_sys_version', {
            self.sql_constants.CONDITION: 'id = %s'
        }, ("version", ))
        if current_version_result is False:
            # 创建表
            sql = """
                CREATE TABLE `tbl_sys_version` (
                  `id` VARCHAR(10) NOT NULL,
                  `value` VARCHAR(45) NOT NULL,
                  PRIMARY KEY (`id`))
                ENGINE = InnoDB
                DEFAULT CHARACTER SET = utf8;
            """.format(target_version)
            yield self.async_pools.execute(sql)
            yield self.async_pools.execute('INSERT INTO `tbl_sys_version` (id, value) VALUES ("version", "{}")'.format(v))
        elif current_version_result and 'value' in current_version_result:
            current_version = current_version_result['value']
            current_version = int(current_version.replace(".", ""))
        else:
            yield self.async_pools.execute('INSERT INTO `tbl_sys_version` (id, value) VALUES ("version", "{}")'.format(v))

        # 3.
        # tx = yield self.async_pools.begin()
        # try:
        target_dir_names = []
        for parent, dir_names, file_names in os.walk("../update/sql/"):
            for dir_name in dir_names:
                try:
                    dir_version = int(dir_name.replace("v", ""))
                except Exception as e:
                    dir_version = 0

                if (current_version < dir_version) and (dir_version <= target_version):
                    target_dir_names.append(dir_name)

        if target_dir_names:
            for dir_name in target_dir_names:
                for parent, dir_names, file_names in os.walk("../update/sql/{}".format(dir_name)):
                    file_names = sorted(file_names, reverse=False)
                    for file_name in file_names:
                        with open(parent + "/" + file_name, "r", encoding="utf-8") as f:
                            sql = ""
                            for line in f.readlines():
                                sql += line

                            self.logger.info(file_name)
                            try:
                                yield self.async_pools.execute(sql)
                            except Exception as e:
                                self.logger.info(e.args)

        # 更新当前版本
        try:
            yield self.async_pools.execute('UPDATE `tbl_sys_version` set value = "{}" where id="version"'.format(v), ())
        except Exception as e:
            self.logger.exception(e)
        #     yield tx.commit()
        # except Exception as e:
        #     yield tx.rollback()
        #     self.logger.exception(e)
