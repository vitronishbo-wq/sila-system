import http from '@/api/http';

const BASE = '/educacao/admin';

export const educacaoAdminService = {
  async listRoles() {
    const res = await http.get(`${BASE}/roles`);
    return res.data;
  },

  async rolePermissions(role: string) {
    const res = await http.get(`${BASE}/roles/${role}/permissions`);
    return res.data;
  },

  async checkScope(params: {
    user_role: string;
    user_province?: string;
    user_municipality?: string;
    user_school?: string;
    resource_nivel: string;
    resource_province?: string;
    resource_municipality?: string;
    resource_school?: string;
  }) {
    const res = await http.get(`${BASE}/scope/check`, { params });
    return res.data;
  },

  async criarMatricula(provider: string, student_id: string, school_id: string,
    municipality_id?: string, province_id?: string) {
    const res = await http.post(`${BASE}/workflows/matricula/criar`, null, {
      params: { provider, student_id, school_id, municipality_id, province_id }
    });
    return res.data;
  },

  async avancarMatricula(provider: string, actor: string) {
    const res = await http.post(`${BASE}/workflows/matricula/avancar`, null, {
      params: { provider, actor }
    });
    return res.data;
  },

  async criarTransferencia(provider: string, student_id: string,
    school_origin_id: string, school_destination_id: string,
    municipality_id?: string, province_id?: string) {
    const res = await http.post(`${BASE}/workflows/transferencia/criar`, null, {
      params: { provider, student_id, school_origin_id, school_destination_id, municipality_id, province_id }
    });
    return res.data;
  },

  async avancarTransferencia(provider: string, actor: string) {
    const res = await http.post(`${BASE}/workflows/transferencia/avancar`, null, {
      params: { provider, actor }
    });
    return res.data;
  },

  async delegatePermission(delegator_role: string, delegator_id: string,
    delegate_role: string, delegate_id: string, permission: string,
    province_id?: string, municipality_id?: string, school_id?: string) {
    const res = await http.post(`${BASE}/delegation/delegate`, null, {
      params: { delegator_role, delegator_id, delegate_role, delegate_id, permission, province_id, municipality_id, school_id }
    });
    return res.data;
  },

  async listDelegations(delegate_id: string) {
    const res = await http.get(`${BASE}/delegation/list/${delegate_id}`);
    return res.data;
  },
};
