#!/usr/bin/env python3
import socket
import logging

#logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)

host = 'ps4'

class Device:
    def __init__(self, name, host, on_active=None):
        self.name = name
        self.host = host
        # Callable to call when state turns True
        self.on_active = on_active
        log.info('%s: on_active: %s', self, self.on_active)
        self.state = None

    def __repr__(self):
        return '{}@{}:{}'.format(self.name, self.host, self.port)

    def is_reachable(self):
        """
        Implementing ICMP Ping seemed like too much work so we'll require a port for now
        """
        up = False
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)
        try:
            s.connect((self.host, self.port))
            up = True
        except socket.error as e:
            pass
        finally:
            s.close()

        log.debug('%s is_reachable: %s', self, up)
        return up


class SourceDevice(Device):
    """
    Device to poll for state with is_active.
    """
    def is_active(self):
        """
        Default implementation of is_active is to just call is_reachable
        """
        res = self.is_reachable()
        log.debug('%s is_active: %s', self, res)
        self.state = res
        return res

class PS4(SourceDevice):
    #DDP_VERSION = '00010010'
    ddp_version = '00020020'
    port = 987

    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        self.latest_response = ''

    def is_reachable(self):
        up = bool(self.query_ps4())
        log.debug('%s is_reachable: %s', self, up)
        return up

    def is_active(self):
        if not self.is_reachable():
            self.state = False
            return False
        res = '200 Ok' in self.latest_response
        self.state = res
        log.debug('%s is_active: %s', self, res)
        return res

    def query_ps4(self):
        """
        Send a special HTTP request over UDP(!)
        Response should be something like "HTTP/1.1 620 Server Standby" or
        "HTTP/1.1 200 Ok"
        """
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(4)
        msg = (
            'SRCH * HTTP/1.1\n'
            'device-discovery-protocol-version:{}'.format(
                self.ddp_version
            )
        )
        try:
            log.debug('Sending:\n%s', msg)
            s.sendto(bytes(msg, 'utf-8'), (self.host, self.port))
        except socket.error as e:
            log.error(e)
            return False

        try:
            res_msg = s.recv(1024)
        except socket.timeout:
            log.warning('Timeout waiting for response from ps4')
            # Probably in transition between standby and on or vice versa
            res_msg = ''
        s.close()
        self.latest_response = str(res_msg)
        return self.latest_response

ps4 = PS4('ps4', host)

if ps4.is_active():
    print('ON')
else:
    print('OFF')