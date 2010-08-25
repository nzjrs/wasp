import logging
import gobject

COMMAND_ACK             = "ACK"
COMMAND_NACK            = "NACK"

COMMAND_ERROR_PENDING   = 0
COMMAND_ERROR_LOST      = 1
COMMAND_ERROR_NACK      = 2

CONTROL_REFRESH_FREQ    = 10

ID_ROLL                 = 0
ID_PITCH                = 1
ID_HEADING              = 2
ID_THRUST               = 3

ID_LIST_FMS_ATTITUDE    = [ID_ROLL, ID_PITCH, ID_HEADING, ID_THRUST]
ID_LIST_FMS_RC          = [ID_ROLL, ID_PITCH, ID_HEADING, ID_THRUST]

ID_RC                   = 0
ID_ATTITUDE             = 1

ID_LIST_FMS_MODE        = [ID_RC, ID_ATTITUDE]

LOG = logging.getLogger("wasp.fms")

class _Command:
    def __init__(self, msgid, ok_cb, failed_cb, delete_myself_cb, timeout=1000):
        self.msgid = msgid
        self.ok_cb = ok_cb
        self.failed_cb = failed_cb
        self.watch = gobject.timeout_add(timeout, self._on_timeout, delete_myself_cb)

    def received(self, msg_name):
        #check we have not timed out
        if self.watch != None:
            if msg_name == COMMAND_ACK:
                self.ok_cb()
            elif msg_name == COMMAND_NACK:
                self.failed_cb(COMMAND_ERROR_NACK)
            else:
                raise Exception("Unknown message name (should be ACK or NACK)")
            #cancel timeout
            self.watch = None

    def _on_timeout(self, delete_myself_cb):
        #check we have not been cancelled
        if self.watch != None:
            self.failed_cb(COMMAND_ERROR_LOST)
            delete_myself_cb(self.msgid)
        self.watch = None
        return False

class CommandManager:
    def __init__(self, communication):
        self.communication = communication
        self.communication.connect("message-received", self._message_received)
        self.pending = {}

    def _message_received(self, comm, msg, header, payload):
        if msg.name in (COMMAND_ACK, COMMAND_NACK):
            msgid = msg.unpack_values(payload)[0]
            try:
                self.pending[msgid].received(msg.name)
                del(self.pending[msgid])
            except KeyError:
                pass

    def _delete_command(self, msgid):
        del(self.pending[msgid])

    def send_command(self, msg, values, ok_cb, failed_cb):
        if not msg.is_command:
            raise Exception("Can only send command messages")

        if msg.id in self.pending:
            failed_cb(COMMAND_ERROR_PENDING)
        else:
            self.pending[msg.id] = _Command(msg.id, ok_cb, failed_cb, self._delete_command)
            self.communication.send_message(msg, values)

class ControlManager:



    def __init__(self, source, messages_file):
        self.source = source
        self.enabled = False

        #cache supported messages
        self._msg_fms_rc = messages_file["FMS_RC"]
        self._msg_fms_attitude = messages_file["FMS_ATTITUDE"]

        #current message and args
        self._msg = None
        self._msg_id = None
        #send FMS messages at regular frequency
        self._timout_id = None

        #setpoints
        self._sp = [
            [0]     * len(ID_LIST_FMS_RC),
            [0.0]   * len(ID_LIST_FMS_ATTITUDE)
        ]

    def _send_control(self):
        if self._msg != None and self._msg_id != None:
            self.source.send_message(self._msg, self._sp[self._msg_id])
        return True

    def enable(self, enable=True):
        #if currently enabled and disabling then remove the source
        if self.enabled and not enable:
            gobject.source_remove(self._timeout_id)
        #else if enabling and not currently enabled then add the source
        elif not self.enabled and enable:
            self._timeout_id = gobject.timeout_add(1000/CONTROL_REFRESH_FREQ, self._send_control)
        self.enabled = enable

    def _generic_set(self, msg, _id, r, p, y, t):
        self._sp[_id][ID_ROLL] = r
        self._sp[_id][ID_PITCH] = p
        self._sp[_id][ID_HEADING] = y
        self._sp[_id][ID_THRUST] = t
        if self._msg != msg and self._msg_id != _id:
            self._msg = msg
            self._msg_id = _id

    def set_attitude(self, roll, pitch, yaw, thrust):
        self._generic_set(
            self._msg_fms_attitude, ID_ATTITUDE,
            roll, pitch, yaw, thrust)

    def set_rc(self, roll, pitch, yaw, thrust, *args):
        self._generic_set(
            self._msg_fms_rc, ID_RC,
            roll, pitch, yaw, thrust)

    def adjust_attitude(self, axis, delta):
        assert axis in ID_LIST_FMS_ATTITUDE
        assert type(delta) == int
        self._sp[ID_ATTITUDE][axis] += delta
        self._msg = self._msg_fms_attitude
        self._msg_id = ID_ATTITUDE


