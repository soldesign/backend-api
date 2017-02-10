from influx import InfluxDBWrapper




################################## Tests for InfluxDBWrapper #############################
Wrapper = InfluxDBWrapper()
influx_count = 0
influx_test = 0

influx_test += 1
if Wrapper.create_db('testdb'):
    influx_count += 1
    print("Test: " + str(influx_test) + " passed.")

influx_test += 1
if not Wrapper.create_db('testdb'):
    influx_count += 1
    print("Test: " + str(influx_test) + " passed.")

influx_test += 1
if Wrapper.insert_config('testdb', 'config', '123'):
    influx_count += 1
    print("Test: " + str(influx_test) + " passed.")

influx_test += 1
if Wrapper.get_config('testdb', '123') == 'config':
    influx_count += 1
    print("Test: " + str(influx_test) + " passed.")

influx_test += 1
if Wrapper.create_user('testuser', 'testpw'):
    influx_count += 1
    print("Test: " + str(influx_test) + " passed.")

influx_test += 1
if not Wrapper.create_user('testuser', 'testpw'):
    influx_count += 1
    print("Test: " + str(influx_test) + " passed.")

influx_test += 1
if not Wrapper.grant_privilege_user('testdb', 'testuse', 'all'):
    influx_count += 1
    print("Test: " + str(influx_test) + " passed.")

influx_test += 1
if Wrapper.grant_privilege_user('testdb', 'testuser', 'all'):
    influx_count += 1
    print("Test: " + str(influx_test) + " passed.")

influx_test += 1
if Wrapper.remove_db('testdb'):
    influx_count += 1
    print("Test: " + str(influx_test) + " passed.")

influx_test += 1
if not Wrapper.remove_db('testdb'):
    influx_count += 1
    print("Test: " + str(influx_test) + " passed.")

influx_test += 1
if Wrapper.remove_user('testuser'):
    influx_count += 1
    print("Test: " + str(influx_test) + " passed.")

influx_test += 1
if not Wrapper.remove_user('testuser'):
    influx_count += 1
    print("Test: " + str(influx_test) + " passed.")


print(str(influx_count) + ' Tests from ' + str(influx_test) + ' Tests passed')

