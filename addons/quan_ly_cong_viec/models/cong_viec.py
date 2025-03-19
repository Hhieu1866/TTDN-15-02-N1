# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class CongViec(models.Model):
    _name = "cong_viec"
    _description = "Công việc"
    _rec_name = "ten_cong_viec"
    _order = "ngay_bat_dau, ma_cong_viec"
    
    ma_cong_viec = fields.Char(string="Mã công việc", required=True, index=True)
    ten_cong_viec = fields.Char(string="Tên công việc", required=True)
    mo_ta = fields.Text(string="Mô tả")
    
    # Thời gian
    ngay_bat_dau = fields.Date(string="Ngày bắt đầu", required=True)
    ngay_ket_thuc = fields.Date(string="Ngày kết thúc")
    
    # Quan hệ
    du_an_id = fields.Many2one('du_an', string="Thuộc dự án", required=True, ondelete='cascade')
    nguoi_phu_trach_id = fields.Many2one('nhan_vien', string="Người phụ trách")
    
    # Các trường quan hệ tham chiếu ngược
    nguoi_tham_gia_ids = fields.One2many('nguoi_tham_gia', 'cong_viec_id', string="Người tham gia")
    bao_cao_tien_do_ids = fields.One2many('bao_cao_tien_do', 'cong_viec_id', string="Báo cáo tiến độ")
    nguon_luc_ids = fields.One2many('phan_bo_nguon_luc', 'cong_viec_id', string="Nguồn lực phân bổ")
    
    # Thông tin tiến độ
    ke_hoach_gio = fields.Float(string="Kế hoạch (giờ)")
    thuc_te_gio = fields.Float(string="Thực tế (giờ)", compute="_compute_thuc_te_gio", store=True)
    tien_do = fields.Float(string="Tiến độ (%)", compute="_compute_tien_do", store=True)
    
    # Độ ưu tiên, trạng thái
    do_uu_tien = fields.Selection([
        ('thap', 'Thấp'),
        ('trung_binh', 'Trung bình'),
        ('cao', 'Cao'),
        ('rat_cao', 'Rất cao')
    ], string="Độ ưu tiên", default='trung_binh')
    
    trang_thai = fields.Selection([
        ('moi', 'Mới'),
        ('dang_thuc_hien', 'Đang thực hiện'),
        ('tam_dung', 'Tạm dừng'),
        ('hoan_thanh', 'Hoàn thành'),
        ('huy_bo', 'Hủy bỏ')
    ], string="Trạng thái", default='moi', tracking=True)
    
    _sql_constraints = [
        ('ma_cong_viec_unique', 'unique(ma_cong_viec)', 'Mã công việc phải là duy nhất!'),
    ]
    
    @api.depends('bao_cao_tien_do_ids', 'bao_cao_tien_do_ids.so_gio')
    def _compute_thuc_te_gio(self):
        for record in self:
            record.thuc_te_gio = sum(record.bao_cao_tien_do_ids.mapped('so_gio'))
    
    @api.depends('bao_cao_tien_do_ids', 'bao_cao_tien_do_ids.tien_do')
    def _compute_tien_do(self):
        for record in self:
            if record.bao_cao_tien_do_ids:
                # Lấy báo cáo tiến độ mới nhất
                bao_cao_moi_nhat = record.bao_cao_tien_do_ids.sorted(key=lambda r: r.ngay_bao_cao, reverse=True)[0]
                record.tien_do = bao_cao_moi_nhat.tien_do
            else:
                record.tien_do = 0
    
    @api.constrains('ngay_bat_dau', 'ngay_ket_thuc')
    def _check_dates(self):
        for record in self:
            if record.ngay_ket_thuc and record.ngay_bat_dau > record.ngay_ket_thuc:
                raise ValidationError(_("Ngày bắt đầu không thể sau ngày kết thúc!"))
    
    @api.constrains('du_an_id', 'ngay_bat_dau', 'ngay_ket_thuc')
    def _check_project_dates(self):
        for record in self:
            if record.du_an_id.ngay_bat_dau and record.ngay_bat_dau < record.du_an_id.ngay_bat_dau:
                raise ValidationError(_("Ngày bắt đầu công việc không thể trước ngày bắt đầu dự án!"))
            
            if record.du_an_id.ngay_ket_thuc and record.ngay_ket_thuc and record.ngay_ket_thuc > record.du_an_id.ngay_ket_thuc:
                raise ValidationError(_("Ngày kết thúc công việc không thể sau ngày kết thúc dự án!"))
